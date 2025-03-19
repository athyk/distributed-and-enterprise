import json
import secrets
import threading
import time

import redis

import grpc
from backend.common.proto import community_pb2, community_pb2_grpc


class CommunityClient:
    """
    A client for interacting with a Community service, handling GRPC and Redis calls.

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
                cls._instance = super(CommunityClient, cls).__new__(cls)
                cls._instance._initialise()
        return cls._instance

    @classmethod
    def initialise(cls, endpoint_url: str, redis_url: str):
        """
        Set the configuration for CommunityClient. This would also handle auth/encryption.

        The intention behind calling this, each service would initialise the client with the endpoint URL.
        Then that would allow caches to be accessed from anywhere.

        :param endpoint_url: URL of the Community service, points to the community instance, e.g. "community-service:50052"
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
            raise ValueError("CommunityClient not initialised")

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
        self._stub = community_pb2_grpc.AccountsStub(self._channel)
        self._redis_client = redis.from_url(self._redis_url)

    def create(self, req: community_pb2.CommunityCreateRequest, session_id: int) -> community_pb2.CommunityIDResponse:
        """
        Create a new community in the Community service.
        """
        print('community creation')
        session_keys = self._redis_client.keys(f"sid:{session_id}:*")
        if not session_keys:
            return community_pb2.BasicCommunityResponse(
                success=False,
                http_status=401,
                error_message=['Action Requires User To Be Logged In']
            )

        user_session = session_keys[0]

        print(user_session)

        return self._grpc_call_with_retry(self._stub.CommunityCreate, req)
    
    def update(self, req: community_pb2.CommunityUpdateRequest) -> community_pb2.BasicCommunityResponse:
        """
        Updates a selected community in the Community service.
        """
        # TODO:


        return self._grpc_call_with_retry(self._stub.CommunityUpdate, req)
    
    def view(self, req: community_pb2.CommunityViewRequest) -> community_pb2.CommunityDataResponse:
        """
        Views a selected community in the Community service.
        """
        # TODO:


        return self._grpc_call_with_retry(self._stub.CommunityView, req)
    
    def delete(self, req: community_pb2.CommunityDeleteRequest) -> community_pb2.BasicCommunityResponse:
        """
        Deletes a community in the Community service.
        """
        # TODO:


        return self._grpc_call_with_retry(self._stub.CommunityDelete, req)

    # noinspection PyMethodMayBeStatic
    def user_to_json(self, user: community_pb2.CommunityDataResponse) -> dict:
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
