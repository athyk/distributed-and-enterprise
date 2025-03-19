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


