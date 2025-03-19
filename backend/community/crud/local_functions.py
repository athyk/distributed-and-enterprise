from backend.community.database.models import CommunityDegree, CommunityTag
from backend.common.services import TagsClient, DegreesClient
from backend.common.proto import tag_pb2, degree_pb2


def add_tags(session, tags, community_id):
    """
    This function searches for the tags provided and connects them to -
    the Community in the CommunityTag table
    """

    tag_client = TagsClient()

    for tag in tags:
        res = tag_client.create(tag_pb2.TagCreateRequest(id=tag))

        if res.success:  # Never assume the tag was created, do not error out either
            user_tag = CommunityTag(community_id=community_id, tag_id=tag)
            session.add(user_tag)

    session.commit()


def add_degrees(session, degrees, community_id):
    """
    This function searches for the degrees provided and connects them to -
    the Community in the CommunityDegree table
    """

    degree_client = DegreesClient()

    for degree in degrees:
        res = degree_client.get(degree_pb2.DegreeGetRequest(id=degree))
        if res.success:
            user_tag = CommunityDegree(community_id=community_id, degree_id=degree)
            session.add(user_tag)

    session.commit()


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


def get_degree_name(degree_id):
    """
    Get a specific degree name
    """
    client = DegreesClient()

    try:
        req = degree_pb2.DegreeGetRequest(
            id=degree_id,
        )

        res: degree_pb2.DegreeGetResponse = client.get(req)

        data = client.degree_to_json(res.degree)

        return data['name']

    except Exception:
        return ''
