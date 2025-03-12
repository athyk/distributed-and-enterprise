from django.urls import path

from .view.degrees.list import list_degrees
from .view.degrees.tags import degree_paths
from .view.tags.list import list_tags
from .view.tags.tags import tag_paths
from .views import chat_message

from backend.core.view.community.community_crud import community_crud_paths, community_creation
from backend.core.view.auth.login import login_user
from backend.core.view.auth.register import register_user


urlpatterns = [
    path('chat/message/', chat_message),
    path('community/<int:community_id>', community_crud_paths),
    path('community/', community_creation),
    path('auth/login', login_user),
    path('auth/register', register_user),
    path('tags/', tag_paths),
    path('tags/list/', list_tags),
    path('degrees/', degree_paths),
    path('degrees/list/', list_degrees),
]