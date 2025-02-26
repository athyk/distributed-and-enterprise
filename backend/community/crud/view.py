from backend.common.files.data_verify import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Community, Tag, Degree, CommunityDegree, CommunityTag, CommunityUser

from math import inf as INFINITY

def get_community_data(community_id):
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)

    data_gathered = {
        'name' : None,
        'description' : None,
        'public' : None,
        'tags' : [],
        'degrees' : []
    }

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

        tag_result = session.query(Tag.name).filter(
            Community.id == community_id,
            Community.id == CommunityTag.community_id,
            CommunityTag.tag_id == Tag.id
        ).all()

        tags = []
        degrees = []

        for tag in tag_result:
            tags.append(str(tag[0]))
        
        degree_result = session.query(Degree.name).filter(
            Community.id == community_id,
            Community.id == CommunityDegree.community_id,
            CommunityDegree.degree_id == Degree.id
        ).all()

        for degree in degree_result:
            degrees.append(degree[0])

        return True, [], name, description, public, tags, degrees
        
