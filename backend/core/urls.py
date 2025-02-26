from django.urls import path
from .views import ping1, ping5, ping10, chat_message

from backend.core.community_views.community_crud_views import community_crud_paths, community_creation

urlpatterns = [
    path('ping/', ping1),
    path('ping/1/', ping1),
    path('ping/5/', ping5),
    path('ping/10/', ping10),
    path('chat/message/', chat_message),
    path('community/<int:community_id>', community_crud_paths),
    path('community/', community_creation),
]