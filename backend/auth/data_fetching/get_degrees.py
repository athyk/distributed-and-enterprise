from backend.auth.database.database import get_db

from backend.auth.database.models import Degree


def get_degrees():
    with get_db() as session:
        degree_result = session.query(Degree.name).all()

        degree_list = []

        for degree in degree_result:
            degree_list.append(degree[0])

        return degree_list