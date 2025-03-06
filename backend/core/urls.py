from django.urls import path
from .views import ping1, ping5, ping10, chat_message

from backend.core.view.community.community_crud import community_crud_paths, community_creation
from backend.core.view.authentication.authentication import login_user, register_user, send_email_verification_code, verify_email_and_account
from backend.core.view.data_fetching.fetch_data_lists import fetch_degrees, fetch_tags


urlpatterns = [
    path('ping/', ping1),
    path('ping/1/', ping1),
    path('ping/5/', ping5),
    path('ping/10/', ping10),
    path('chat/message/', chat_message),
    path('community/<int:community_id>', community_crud_paths),
    path('community/', community_creation),
    path('authorisation/login', login_user),
    path('authorisation/register', register_user),
    path('authorisation/email/send-code', send_email_verification_code),
    path('authorisation/email/verify', verify_email_and_account),
    path('degrees', fetch_degrees),
    path('tags', fetch_tags),
]