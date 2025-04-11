import threading
import time

import redis

import grpc
from backend.common.proto import tag_pb2, tag_pb2_grpc


class TagsClient:
    """
    A client for interacting with a Tags service, handling GRPC and Redis calls.

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
                cls._instance = super(TagsClient, cls).__new__(cls)
                cls._instance._initialise()
        return cls._instance

    @classmethod
    def initialise(cls, endpoint_url: str, redis_url: str):
        """
        Set the configuration for TagsClient. This would also handle auth/encryption.

        The intention behind calling this, each service would initialise the client with the endpoint URL.
        Then that would allow caches to be accessed from anywhere.

        :param endpoint_url: URL of the Tag service, points to the tag instance, e.g. "tag-service:50053"
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
            raise ValueError("TagsClient not initialised")

        self._endpoint_url = self._config["endpoint_url"]
        self._redis_url = self._config["redis_url"]
        self._reconnect()

    def _grpc_call_with_retry(self, grpc_call, *args, **kwargs):
        max_retries = 3
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
        self._stub = tag_pb2_grpc.TagsStub(self._channel)
        self._redis_client = redis.from_url(self._redis_url)

    def create(self, req: tag_pb2.TagCreateRequest) -> tag_pb2.TagCreateResponse:
        """
        Create or use an existing tag in the Tag service.

        Specify update only if you only want to get pre-existing tags.
        """
        # TODO: add/update cache
        return self._grpc_call_with_retry(self._stub.Create, req)

    def delete(self, req: tag_pb2.TagDeleteRequest) -> tag_pb2.TagDeleteResponse:
        """
        Delete a tag from the Tag service.

        Intended for admins.
        """
        # TODO: remove from cache
        return self._grpc_call_with_retry(self._stub.Delete, req)

    def get(self, req: tag_pb2.TagGetRequest) -> tag_pb2.TagGetResponse:
        """
        Get a tag from the Tag service.
        """
        # TODO: add cache
        return self._grpc_call_with_retry(self._stub.Get, req)

    def list(self, req: tag_pb2.TagListRequest) -> tag_pb2.TagListResponse:
        """
        List tags from the Tag service.
        """
        # TODO: add cache
        return self._grpc_call_with_retry(self._stub.List, req)

    # noinspection PyMethodMayBeStatic
    def tag_to_json(self, tag: tag_pb2.Tag) -> dict:
        """
        Format the tag object into a dictionary for use in a JSON response.

        :param tag: The tag object to format
        :return: A dictionary containing the tag's details
        """
        return {
            "id": tag.id,
            "name": tag.name,
            "count": tag.count,
            "created_at": tag.created_at,
            "updated_at": tag.updated_at,
        }
