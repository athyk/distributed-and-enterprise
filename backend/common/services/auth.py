import os
import string
import threading

import grpc

from backend.common.proto import auth_pb2_grpc, auth_pb2


REQUIRED_UNIVERSITY_DOMAIN = os.getenv("UNIVERSITY_DOMAIN", "uwe.ac.uk")


class AuthClient:
    """
    A client for interacting with an Auth service, handling GRPC calls.

    This would also handle any additional caching for per operations.

    Validation can be done here as it's all internal, as it's not a security-first project.
    Since this is still all server side.

    Ensuring that only one instance of the client is created, and that the client is thread-safe.
    """
    _instance = None
    _channel = None
    _lock = threading.Lock()

    _config = {}

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AuthClient, cls).__new__(cls)
                cls._instance._initialise()
        return cls._instance

    @classmethod
    def initialise(cls, endpoint_url: str):
        """
        Set the configuration for AuthClient. This would also handle auth/encryption.

        :param endpoint_url: URL of the Auth service, points to the auth instance, e.g. "auth-service:50053"
        """
        cls._config = {
            "endpoint_url": endpoint_url,
        }

    def _initialise(self):
        """
        Initialise the GRPC client.
        """
        if not self._config:
            raise ValueError("AuthClient not initialised")

        self._endpoint_url = self._config["endpoint_url"]

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
                ('grpc.keepalive_time_ms', 120000),
                # How many pings can the client send before needing to send a data/header
                # frame? (0 indicates that an infinite number of pings can
                #   be sent without sending a data frame or header frame).
                # If experiment "max_pings_wo_data_throttle" is enabled, instead of pings being
                #   completely blocked, they are throttled.
                ('grpc.http2.max_pings_without_data', 0),
                # If set to zero, disables use of http proxies. Enabled by default
                ('grpc.enable_http_proxy', 0)
            ])

        self._stub = auth_pb2_grpc.AuthStub(self._channel)

    def register_user(self, req: auth_pb2.RegistrationRequest) -> auth_pb2.LoginResponse:
        """
        Create/register a new user in the Auth service.

        :param req: The RegistrationRequest object containing the user's details
        :return: The GRPC response from the Auth service
        """
        # Require the raw request object, as when changes are made to the proto file, it takes less writing
        # to update where it is used.

        # Use individual if statements as it's faster than using a list comprehension
        # Do validation in the handler as it doesn't take up bandwidth when done in the handler
        # compared to sending it across the network to the service and back
        if not self.ensure_valid_email(REQUIRED_UNIVERSITY_DOMAIN, req.email):
            return auth_pb2.LoginResponse(
                success=False,
                http_status=400,
                error_message=["Email must be a valid academic email."],
            )

        # Obviously spamming network requests for invalid passwords is bad.
        # So have a simple check here to prevent that. Here could also be a way to enforce password policies.
        if len(req.password) < 8:
            return auth_pb2.LoginResponse(
                success=False,
                http_status=400,
                error_message=["Password must be at least 8 characters long."],
            )

        # TODO: verify the degree_id and tags are valid, will work for now as it's a placeholder
        # This would wait on a CommunityClient to be created and then call the CommunityClient to have functions
        # for degrees and tags.

        # Now that we believe it's a valid request, we send it along for creation
        return self._stub.UserRegister(req)

    def login_user(self, req: auth_pb2.LoginRequest) -> auth_pb2.LoginResponse:
        """
        Login in a user with the Auth service.

        :param req: The LoginRequest object containing the user's details
        :return: The GRPC response from the Auth service
        """
        if not self.ensure_valid_email(REQUIRED_UNIVERSITY_DOMAIN, req.email):
            return auth_pb2.LoginResponse(
                success=False,
                http_status=400,
                error_message=["Email must be a valid academic email."],
            )

        # Passwords are not validated here, as it's service specific.

        return self._stub.UserLogin(req)

    def verify_login(self, req: auth_pb2.LoginVerificationRequest) -> auth_pb2.LoginVerificationResponse:
        """
        Verify a user's login or registration with the Auth service.

        This can be /login/verify or /register/verify depending on the request.

        :param req: The LoginVerificationRequest object containing the user's details
        :return: The GRPC response from the Auth service
        """
        if not req.otp or len(req.otp) != 6:
            return auth_pb2.LoginVerificationResponse(
                success=False,
                http_status=400,
                error_message=["OTP must be 6 characters long."],
            )

        # Could have a cache of users that were just gone through the login/registration process
        # which would simplify incorrect OTPs, reducing the load on the database.

        # Don't add otp validation here as it's service specific.

        return self._stub.UserLoginVerification(req)

    # TODO: Add in update, delete, and fetch functions with caching.

    # noinspection PyMethodMayBeStatic
    def ensure_valid_email(self, required_domain: str, email: str) -> bool:
        """
        This function checks if the email is valid.

        This is here, rather than the service so that is can be used by the handler

        :param required_domain:
        :param email:
        :return:
        """
        # all emails must have an '@' symbol
        #
        # Use count before splitting to prevent DOS attacks, similar to CVE-2025-22868
        # While split does allow max splits, here is more readable/auditable.
        #
        # also do not use self.email as this is intended to be used across different services/requests
        # so the email should be passed in as a parameter
        if '@' not in email or email.count('@') != 1:
            return False

        # Get the domain of the email, an attacker could use google.com.general@example.com to bypass a simple
        # email check.
        parts = email.split('@')
        username = parts[0]
        domain = parts[1]

        # Use "not in" over "!=" to allow for subdomains such as "mail.google.com"
        if required_domain not in domain:
            return False

        # While regex would have been expensive, a simpler regex compared to regex such as https://regex101.com/r/gJ7pU0/1
        # is much less expensive. However, if statements are faster than regex.
        allowed_chars = set(string.ascii_letters + string.digits + "._%+-")

        for char in username:
            if char not in allowed_chars:
                return False

        return True

    # noinspection PyMethodMayBeStatic
    def user_to_json(self, user: auth_pb2.User) -> dict:
        """
        Format the user object into a dictionary for use in a JSON response.

        :param user: The user object to format
        :return: A dictionary containing the user's details
        """

        return {
            "id": user.id,
            "email": user.email,
            "email_verified": user.email_verified,
            "full_name": user.full_name,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "nickname": user.nickname,
            "gender": user.gender,
            "dob": user.dob,
            "picture_url": user.picture_url,
            "degree_id": user.degree_id,
            "year_of_study": user.year_of_study,
            "grad_date": user.grad_date,
            "tags": list(user.tags),
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }


