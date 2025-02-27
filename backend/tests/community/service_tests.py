import unittest
import random
import string
from unittest.mock import MagicMock
import grpc
from backend.common.proto import community_pb2 #, community_pb2_grpc
from backend.community.services.community_crud import Community_CRUD_Service
from backend.tests.custom_test_assertions import CustomTestCase

from backend.community.crud.view import get_community_data
from backend.community.crud.update import update_community
from backend.community.crud.delete import delete_community


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


class TestCommunityCRUDService(CustomTestCase):
    def test_community_create_success(self):

        random_string = generate_random_string(12)
        
        service = Community_CRUD_Service()
        request = community_pb2.CommunityCreateRequest(
            name=random_string,
            description="A test description",
            public=True,
            tags=["Tag 1", "Tag 2"],
            degrees=["Degree 1", "Degree 2"],
            user_id=1
        )
        context = MagicMock(spec=grpc.ServicerContext)

        response = service.CommunityCreate(request, context)

        self.assertTrueTraceless(response.success)
        self.assertEqualTraceless(response.http_status, 201)
        self.assertGreaterTraceless(response.id, 0)
        self.assertEqualTraceless(response.error_message[0], "Community Successfully Created")


    def test_community_create_failure(self):
        service = Community_CRUD_Service()
        request = community_pb2.CommunityCreateRequest(
            name="",
            description="",
            public=True,
            tags=[],
            degrees=[],
            user_id=42
        )
        context = MagicMock(spec=grpc.ServicerContext)
        
        response = service.CommunityCreate(request, context)
        
        self.assertFalseTraceless(response.success)
        self.assertEqualTraceless(response.http_status, 400)
        self.assertEqualTraceless(response.id, -1)
        self.assertEqualTraceless(response.error_message, ['Minimum String Len Expected: 4 | Received: 0 | Data: ',
                                                           'Minimum String Len Expected: 4 | Received: 0 | Data: '])
        

    def test_community_view_success(self):
        service = Community_CRUD_Service()
        request = community_pb2.CommunityViewRequest(
            id=1
        )
        context = MagicMock(spec=grpc.ServicerContext)

        response = service.CommunityView(request, context)

        self.assertTrueTraceless(response.success)
        self.assertEqualTraceless(response.http_status, 200)
        self.assertEqualTraceless(response.error_message, [])
        self.assertEqualTraceless(response.name, 'Community')
        self.assertEqualTraceless(response.description, 'Desc')
        self.assertTrueTraceless(response.public_community)
        self.assertEqualTraceless(response.tags, [])
        self.assertEqualTraceless(response.degrees, [])

    
    def test_community_view_failure(self):
        service = Community_CRUD_Service()
        request = community_pb2.CommunityViewRequest(id=2)
        context = MagicMock(spec=grpc.ServicerContext)

        response = service.CommunityView(request, context)

        self.assertFalseTraceless(response.success)
        self.assertEqualTraceless(response.http_status, 400)
        self.assertEqualTraceless(response.error_message, ["Selected community does not exist"])
        self.assertEqualTraceless(response.name, '')
        self.assertEqualTraceless(response.description, '')
        self.assertFalseTraceless(response.public_community)
        self.assertEqualTraceless(response.tags, [])
        self.assertEqualTraceless(response.degrees, [])


    def test_community_update_success(self):
        service = Community_CRUD_Service()
        request = community_pb2.CommunityUpdateRequest(
            id=1,
            name="Community",
            description="Desc",
            public=True,
            tags=[],
            degrees=[],
            user_id=1
        )
        context = MagicMock(spec=grpc.ServicerContext)

        response = service.CommunityUpdate(request, context)

        self.assertTrueTraceless(response.success)
        self.assertEqualTraceless(response.http_status, 200)
        self.assertEqualTraceless(response.error_message, ['Community Successfully Updated'])

    
    def test_community_update_failure(self):
        service = Community_CRUD_Service()
        request = community_pb2.CommunityUpdateRequest(
            id=2,
            name="Community",
            description="Desc",
            public=True,
            tags=[],
            degrees=[],
            user_id=1
        )
        context = MagicMock(spec=grpc.ServicerContext)

        response = service.CommunityUpdate(request, context)

        self.assertFalseTraceless(response.success)
        self.assertEqualTraceless(response.http_status, 400)
        self.assertEqualTraceless(response.error_message, ['User Or Community Does Not Exist'])


    def test_community_delete_success(self):
        service = Community_CRUD_Service()
        request = community_pb2.CommunityDeleteRequest(
            id=300,
            user_id=1
        )
        context = MagicMock(spec=grpc.ServicerContext)

        response = service.CommunityDelete(request, context)

        self.assertTrueTraceless(response.success)
        self.assertEqualTraceless(response.http_status, 200)
        self.assertEqualTraceless(response.error_message, ['Community Successfully Deleted'])

    
    def test_community_delete_failure(self):
        service = Community_CRUD_Service()
        request = community_pb2.CommunityDeleteRequest(
            id=2,
            user_id=1
        )
        context = MagicMock(spec=grpc.ServicerContext)

        response = service.CommunityDelete(request, context)

        self.assertFalseTraceless(response.success)
        self.assertEqualTraceless(response.http_status, 400)
        self.assertEqualTraceless(response.error_message, ['User Or Community Does Not Exist'])


if __name__ == '__main__':
    unittest.main()
