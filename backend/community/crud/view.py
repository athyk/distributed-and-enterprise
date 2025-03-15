from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Community, CommunityDegree, CommunityTag

from math import inf as INFINITY


def get_community_data(community_id: int) -> tuple[bool, list, str, str, bool, list, list]:
    """
    This function verifies incoming data and returns the specified community data
    If any errors arise then relevant error messages are returned.
    """

    community_verify, community_error = verify_integer(community_id, 1, INFINITY)

    if False in [community_verify]:

        all_errors = [community_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages, "", "", False, [], []
    
    with get_db() as session:
        result = session.query(Community.name, Community.description, Community.public).filter(Community.id == community_id).first()

        if not result:
            return False, ['Selected community does not exist'], "", "", False, [], []
        
        name = result[0]
        description = result[1]
        public = result[2]

        tag_result = session.query(CommunityTag.tag_id).filter(
            CommunityTag.community_id == community_id
        ).all()

        tags = []
        degrees = []

        for tag in tag_result:
            tags.append(str(tag[0]))
        
        degree_result = session.query(CommunityDegree.degree_id).filter(
            CommunityDegree.community_id == community_id
        ).all()

        for degree in degree_result:
            degrees.append(degree[0])

        return True, [], name, description, public, tags, degrees
        
