from backend.common.services import TagsClient
from backend.common.proto import tag_pb2


def get_tag_name(tag_id):
    """
    Get a specific tag name
    """
    client = TagsClient()

    try:
        req = tag_pb2.TagGetRequest(
            id=tag_id,
        )

        res: tag_pb2.TagGetResponse = client.get(req)

        data = client.tag_to_json(res.tag)

        return data['name']

    except Exception:
        return ''
