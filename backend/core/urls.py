from django.urls import path
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
]