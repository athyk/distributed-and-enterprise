import json
import secrets
import threading
import time

import redis

import grpc
from backend.common.proto import accounts_pb2, accounts_pb2_grpc


class AccountsClient:
    """
    A client for interacting with an Accounts service, handling GRPC and Redis calls.

    This would also handle any additional caching for per operations.

    Ensuring that only one instance of the client is created, and that the client is thread-safe.
    """
    _instance = None
    _channel = None
    _redis_client = None
    _lock = threading.Lock()

    _config = {}

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AccountsClient, cls).__new__(cls)
                cls._instance._initialise()
        return cls._instance

    @classmethod
    def initialise(cls, endpoint_url: str, redis_url: str):
        """
        Set the configuration for AccountsClient. This would also handle auth/encryption.

        The intention behind calling this, each service would initialise the client with the endpoint URL.
        Then that would allow caches to be accessed from anywhere.

        :param endpoint_url: URL of the Auth service, points to the auth instance, e.g. "auth-service:50053"
        :param redis_url: URL of the Redis service, points to the redis instance, e.g. "redis://localhost:6379/0"
        """
        cls._config = {
            "endpoint_url": endpoint_url,
            "redis_url": redis_url,
        }

    def _initialise(self):
        """
        Initialise the GRPC client.
        """
        if not self._config:
            raise ValueError("AccountsClient not initialised")

        self._endpoint_url = self._config["endpoint_url"]
        self._redis_url = self._config["redis_url"]
        self._reconnect()

    def _grpc_call_with_retry(self, grpc_call, *args, **kwargs):
        max_retries = 1
        backoff_factor = 0.5

        for attempt in range(max_retries):
            try:
                return grpc_call(*args, **kwargs)
            except grpc.RpcError as e:
                if "InactiveRpcError" in str(e):
                    if attempt < max_retries - 1:
                        sleep_time = backoff_factor * (2 ** attempt)
                        time.sleep(sleep_time)
                        self._reconnect()
                    else:
                        raise e
                else:
                    raise e

    def _reconnect(self):
        """
        Reconnect or connect to the gRPC channel.
        """
        # TODO: make a secure_channel https://grpc.github.io/grpc/python/grpc.html#grpc.secure_channel
        self._channel = grpc.insecure_channel(
            self._endpoint_url,
            # For options see https://github.com/grpc/grpc/blob/v1.70.x/include/grpc/impl/channel_arg_names.h
            options=[
                # Maximum time that a channel may have no outstanding rpcs, after which the
                #   server will close the connection. Int valued, milliseconds.
                ('grpc.max_connection_idle_ms', 60000),
                # After a duration of this time the client/server pings its peer to see if the
                #   transport is still alive. Int valued, milliseconds.
                ('grpc.keepalive_time_ms', 6000),
                # How many pings can the client send before needing to send a data/header
                # frame? (0 indicates that an infinite number of pings can
                #   be sent without sending a data frame or header frame).
                # If experiment "max_pings_wo_data_throttle" is enabled, instead of pings being
                #   completely blocked, they are throttled.
                ('grpc.http2.max_pings_without_data', 0),
                # If set to zero, disables use of http proxies. Enabled by default
                ('grpc.enable_http_proxy', 0)
            ])
        self._stub = accounts_pb2_grpc.AccountsStub(self._channel)
        self._redis_client = redis.from_url(self._redis_url)

    def register(self, req: accounts_pb2.RegistrationRequest) -> accounts_pb2.LoginResponse:
        """
        Create/register a new user in the Account service.
        """
        # TODO: add cache - a user is highly likely to be fetched after being created
        return self._grpc_call_with_retry(self._stub.Register, req)

    def login(self, req: accounts_pb2.LoginRequest) -> accounts_pb2.LoginResponse:
        """
        Login in a user with the Account service.

        :param req: The LoginRequest object containing the user's details
        :return: The GRPC response from the Account service
        """
        # TODO: remove from cache, as the user may not need to be fetched after login
        return self._grpc_call_with_retry(self._stub.Login, req)

    def get(self, req: accounts_pb2.GetRequest) -> accounts_pb2.GetResponse:
        """
        Get a user from the Account service.
        """
        return self._grpc_call_with_retry(self._stub.Get, req)

    def update(self, req: accounts_pb2.UpdateRequest) -> accounts_pb2.Response:
        """
        Update a user in the Account service.
        """
        return self._grpc_call_with_retry(self._stub.Update, req)

    def delete(self, req: accounts_pb2.DeleteRequest) -> accounts_pb2.Response:
        """
        Delete a user in the Account service as well as delete their sessions.
        """
        res: accounts_pb2.Response = self._grpc_call_with_retry(self._stub.Delete, req)

        if not res.success:
            return res

        self.logout_user(req.user_id)

        return res

    def create_session(self, user: accounts_pb2.User) -> tuple[str, int]:
        """
        Create a user session, after the user has been registered or logged in.

        :param user: The user object containing the user's details (from the Account service)
        :return: A tuple containing the session ID and the timeout for the session
        """

        session_id = secrets.token_urlsafe(32)

        timeout = 36000  # 10 hour, timeout is in seconds, maybe config?

        # Set the JSON user object in the cache, with the session ID as the key
        # This allows for quick access to the user object from the session ID
        self._redis_client.set(
            name=f"sid:{session_id}:{user.id}",
            value=json.dumps(self.user_to_json(user)),
            ex=timeout,
        )
        return session_id, timeout

    def check_session(self, session_id: str) -> dict | None:
        """
        Check if a user session is valid.

        :param session_id: The session ID to check
        :return: The user object if the session is valid, otherwise None
        """
        session_keys = self._redis_client.keys(f"sid:{session_id}:*")
        if not session_keys:
            return None

        res = self._redis_client.get(session_keys[0])

        if not res:
            return None

        res = json.loads(res)

        return res

    def logout_session(self, session_id: str) -> bool:
        """
        Log out a user by removing the session from the cache.

        :param session_id: The session ID to remove
        :return: True if the session was removed, otherwise False
        """
        session_keys = self._redis_client.keys(f"sid:{session_id}:*")
        if not session_keys:
            return False

        for key in session_keys:
            self._redis_client.delete(key)

        return True

    def logout_user(self, user_id: int) -> bool:
        """
        Log out a user by removing all their sessions from the cache.

        This is the same as "Log out from all devices".

        :param user_id: The user ID to remove sessions for
        :return: True if the sessions were removed, otherwise False
        """
        session_keys = self._redis_client.keys(f"sid:*:{user_id}")
        if not session_keys:
            return False

        for key in session_keys:
            self._redis_client.delete(key)

        return True

    def save_otp(self, user_id: int, otp_seed: str) -> None:
        """
        Save the OTP for the user in the cache.

        :param user_id: The user ID to save the OTP for
        :param otp_seed: The OTP Seed that allows the matching of the OTP
        """
        # Save the OTP in the cache, with the user ID as the key
        self._redis_client.set(
            name=f"otp:{user_id}",
            value=otp_seed,
            ex=300,  # 5 minutes
        )

    def get_otp(self, user_id: int) -> str | None:
        """
        Get the OTP for the user from the cache.

        :param user_id: The user ID to get the OTP for
        :return: The OTP Seed if it exists, otherwise None
        """
        return self._redis_client.get(f"otp:{user_id}")

    # noinspection PyMethodMayBeStatic
    def user_to_json(self, user: accounts_pb2.User) -> dict:
        """
        Format the user object into a dictionary for use in a JSON response.

        :param user: The user object to format
        :return: A dictionary containing the user's details
        """
        return {
            "id": user.id,
            "email": user.email,
            "email_verified": user.email_verified,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "gender": user.gender,
            "date_of_birth": user.date_of_birth,
            "picture_url": user.picture_url,
            "degree_id": user.degree_id,
            "year_of_study": user.year_of_study,
            "grad_date": user.grad_date,
            "tags": list(user.tags),
            "rank": user.rank,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
