from backend.auth.database.database import get_db

from backend.auth.database.models import Tag


def get_tags():
    with get_db() as session:
        degree_result = session.query(Tag.name).all()

        degree_list = []

        for degree in degree_result:
            degree_list.append(degree[0])

        return degree_list
