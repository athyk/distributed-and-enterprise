from backend.community.database.models import EventTag
from backend.common.services import TagsClient
from backend.common.proto import tag_pb2
import requests
import os


def add_tags(session, tags, event_id):
    """
    This function searches for the tags provided and connects them to -
    the Announcement in the AnnouncementTag table
    """

    tag_client = TagsClient()

    for tag in tags:
        res = tag_client.create(tag_pb2.TagCreateRequest(id=tag))

        if res.success:  # Never assume the tag was created, do not error out either
            user_tag = EventTag(event_id=event_id, tag_id=tag)
            session.add(user_tag)

    session.commit()


def location_name_to_coords(place_name: str) -> tuple[bool, float, float, list]:
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place_name}&key={os.environ.get('GEOCODING_API_KEY')}"
    response = requests.get(url).json()

    if response["status"] == "OK":
        location = response["results"][0]["geometry"]["location"]
        lng = location["lng"]
        lat = location["lat"]

        return True, lng, lat, []

    else:
        print("Error:", response["status"])
        return False, None, None, ['Unable To Find Location']
