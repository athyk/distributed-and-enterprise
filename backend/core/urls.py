from django.urls import path

from .view.auth.verify import verify
from .view.auth.login import login_user
from .view.auth.register import register_user
from .views import ping1, ping5, ping10, chat_message

from backend.core.view.community.community_crud import community_crud_paths, community_creation


urlpatterns = [
    path('ping/', ping1),
    path('ping/1/', ping1),
    path('ping/5/', ping5),
    path('ping/10/', ping10),
    path('chat/message/', chat_message),
    path('community/<int:community_id>', community_crud_paths),
    path('community/', community_creation),

    path('auth/login', login_user),
    path('auth/login/verify', verify),
    path('auth/register', register_user),
    path('auth/register/verify', verify),
]
