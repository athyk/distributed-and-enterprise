from django.urls import path

from .view.auth.logout import logout_self
from .view.degrees.list import list_degrees
from .view.degrees.degrees import degree_paths
from .view.post.create_attachment import create_attachment
from .view.post.list import list_posts
from .view.post.posts import post_paths
from .view.tags.list import list_tags
from .view.tags.tags import tag_paths
from .view.users.self.profile import update_profile_picture
from .view.users.self.users import user_self_paths
from .view.users.users import user_paths

from backend.core.view.community.announcements import community_announcement_paths, community_announcement_action_paths, community_global_announcement_view
from backend.core.view.community.community_events import community_event_action_paths, community_event_paths, community_global_event_view
from backend.core.view.community.community_crud import community_crud_paths, community_creation
from backend.core.view.community.community_joins import community_join_actions, invite_to_community
from backend.core.view.community.searching import fetch_communities
from backend.core.view.community.member_management import community_promotion, community_ban, community_demotion


from backend.core.view.auth.login import login_user
from backend.core.view.auth.register import register_user


urlpatterns = [
    path('auth/login', login_user),
    path('auth/register', register_user),
    path('auth/logout', logout_self),
    path('users/@me/profile', update_profile_picture),
    path('users/@me', user_self_paths),
    path('users/', user_paths),

    path('tags/', tag_paths),
    path('tags/list/', list_tags),

    path('degrees/', degree_paths),
    path('degrees/list/', list_degrees),

    path('community/<int:community_id>', community_crud_paths),
    path('community/', community_creation),
    path('community/announcements', community_global_announcement_view),
    path('community/<int:community_id>/announcements', community_announcement_paths),
    path('community/<int:community_id>/announcements/<int:announcement_id>', community_announcement_action_paths),
    path('community/<int:community_id>/members', community_join_actions),
    path('community/<int:community_id>/invite', invite_to_community),
    path('community/<int:community_id>/ban', community_ban),
    path('community/<int:community_id>/promote', community_promotion),
    path('community/<int:community_id>/demote', community_demotion),
    path('community/events', community_global_event_view),
    path('community/<int:community_id>/events', community_event_paths),
    path('community/<int:community_id>/events/<int:event_id>', community_event_action_paths),
    path('community/search', fetch_communities),

    path('posts/upload', create_attachment),
    path('posts/list', list_posts),
    path('posts/', post_paths),
]
