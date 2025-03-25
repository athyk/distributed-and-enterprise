from datetime import datetime, UTC
from math import inf

import grpc

from backend.accounts.database.database import get_db
from backend.accounts.database.models import PostTag, Post, PostImage
from backend.common.proto import account_post_pb2_grpc, account_post_pb2, tag_pb2
from backend.common.services import TagsClient
from backend.common.utils import verify_string, verify_integer, verify_list


class AccountsPostsServicer(account_post_pb2_grpc.AccountPostsServicer):
    def Create(self, req: account_post_pb2.AccountPostCreateRequest,
               context: grpc.ServicerContext) -> account_post_pb2.AccountPostResponse:
        """
        Create creates a new post
        """
        user_verify, user_error = verify_integer(req.user_id, 1, inf, 'User ID')
        title_verify, title_error = verify_string(req.title, 4, 128, 'Title')
        description_verify, description_error = verify_string(req.description, 4, 2048, 'Description')
        tags_verify, tags_error = verify_list(list(req.tags), 0, 5, 'Tags')
        images_verify, images_error = verify_list(list(req.images), 0, 5, 'Images')

        if False in [user_verify, title_verify, description_verify, tags_verify, images_verify]:

            all_errors = [user_error, title_error, description_error, tags_error, images_error]
            error_messages = [item for item in all_errors if item.strip()]
            return account_post_pb2.AccountPostResponse(success=False, http_status=400, error_message=error_messages)

        with get_db() as session:
            post = Post(
                user_id=req.user_id,
                title=req.title,
                description=req.description,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC)
            )

            session.add(post)
            session.commit()

            # Add tags to the post
            # They assume the tag was already created with the name, similar to how community announcements.
            # Not worth changing this is to take in raw tag names and create them here.
            # As it should be easy to do announcements and posts.
            tag_client = TagsClient()

            for tag in req.tags:
                res = tag_client.create(tag_pb2.TagCreateRequest(id=tag))

                if res.success:  # Never assume the tag was created, do not error out either
                    user_tag = PostTag(post_id=post.id, tag_id=tag)
                    session.add(user_tag)

            session.commit()

            for image in req.images:
                image = PostImage(post_id=post.id, image_url=image)
                session.add(image)

            session.commit()

            post = session.query(Post).filter(Post.id == post.id).first()
            return account_post_pb2.AccountPostResponse(success=True, http_status=201, error_message=['Post Successfully Created'], post=post.to_dict())

    def update_tags(self, session, post_id, tags):
        """
        Update the tags for a post
        """
        post_tags = session.query(PostTag).filter(PostTag.post_id == post_id).all()
        post_tags = [tag.tag_id for tag in post_tags]
        tags_to_add = [tag for tag in tags if tag not in post_tags]
        tags_to_remove = [tag for tag in post_tags if tag not in tags]

        for tag in tags_to_add:
            user_tag = PostTag(post_id=post_id, tag_id=tag)
            session.add(user_tag)

        for tag in tags_to_remove:
            user_tag = session.query(PostTag).filter(PostTag.post_id == post_id, PostTag.tag_id == tag).first()
            session.delete(user_tag)

    def update_images(self, session, post_id, images):
        """
        Update the images for a post
        """
        post_images = session.query(PostImage).filter(PostImage.post_id == post_id).all()
        post_images = [image.image_url for image in post_images]
        images_to_add = [image for image in images if image not in post_images]
        images_to_remove = [image for image in post_images if image not in images]

        for image in images_to_add:
            image = PostImage(post_id=post_id, image_url=image)
            session.add(image)

        for image in images_to_remove:
            image = session.query(PostImage).filter(PostImage.post_id == post_id, PostImage.image_url == image).first()
            session.delete(image)

    def Update(self, req: account_post_pb2.AccountPostUpdateRequest,
               context: grpc.ServicerContext) -> account_post_pb2.AccountPostResponse:
        """
        Update updates a specified post
        """
        # Only the user who created the post can update it.
        user_verify, user_error = verify_integer(req.user_id, 1, inf, 'User ID')
        title_verify, title_error = verify_string(req.title, 4, 128, 'Title')
        description_verify, description_error = verify_string(req.description, 4, 2048, 'Description')
        tags_verify, tags_error = verify_list(list(req.tags), 0, 5, 'Tags')
        images_verify, images_error = verify_list(list(req.images), 0, 5, 'Images')

        if False in [user_verify, title_verify, description_verify, tags_verify, images_verify]:
            all_errors = [user_error, title_error, description_error, tags_error, images_error]
            error_messages = [item for item in all_errors if item.strip()]
            return account_post_pb2.AccountPostResponse(success=False, http_status=400, error_message=error_messages)

        with get_db() as session:
            post_res = session.query(Post).filter(Post.id == req.post_id).first()

            if post_res is None:
                return account_post_pb2.AccountPostResponse(success=False, http_status=400, error_message=['Post selected does not exist'])

            if post_res.user_id != req.user_id:
                return account_post_pb2.AccountPostResponse(success=False, http_status=400, error_message=['Post does not belong to user'])

            post_res.title = req.title
            post_res.description = req.description
            post_res.updated_at = datetime.now(UTC)

            tag_res = session.query(PostTag).filter(PostTag.id == req.post_id).all()

            for tag in tag_res:
                session.delete(tag)

            session.commit()

            self.update_tags(session, req.post_id, req.tags)
            self.update_images(session, req.post_id, req.images)

            session.commit()

            post = session.query(Post).filter(Post.id == req.post_id).first()
            return account_post_pb2.AccountPostResponse(success=True, http_status=200, error_message=['Post Successfully Updated'], post=post.to_dict())

    def List(self, req: account_post_pb2.AccountPostListRequest,
             context: grpc.ServicerContext) -> account_post_pb2.AccountPostListResponse:
        """
        List fetches all/selected number of posts from a user or tag or in general
        """
        if req.limit < 1:
            req.limit = 1
        elif req.limit > 50:
            req.limit = 50
        if req.offset < 0:
            req.offset = 0

        with get_db() as session:
            posts = session.query(Post)

            if req.user_id != 0:
                posts = posts.filter(Post.user_id == req.user_id)

            if req.tag_id != 0:
                posts = posts.join(PostTag).filter(PostTag.tag_id == req.tag_id)
                print('getting tags')

            if req.title != "":
                posts = posts.filter(Post.title.ilike(f'%{req.title}%'))
            if req.description != "":
                posts = posts.filter(Post.description.ilike(f'%{req.description}%'))

            res = posts.order_by(Post.created_at.desc()).limit(req.limit).offset(req.offset).all()

            posts = [post.to_dict() for post in res]

            

            return account_post_pb2.AccountPostListResponse(success=True, http_status=200, error_message=['Posts Successfully Fetched'], posts=posts)

    def Get(self, req: account_post_pb2.AccountPostGetRequest,
            context: grpc.ServicerContext) -> account_post_pb2.AccountPostResponse:
        """
        Get fetches a specified post
        """
        if req.post_id == 0:
            return account_post_pb2.AccountPostResponse(success=False, http_status=400, error_message=['Post ID is Required'])

        with get_db() as session:
            post_res = session.query(Post).filter(Post.id == req.post_id).first()

            if post_res is None:
                return account_post_pb2.AccountPostResponse(success=False, http_status=400, error_message=['Post selected does not exist'])

            return account_post_pb2.AccountPostResponse(success=True, http_status=200, error_message=['Post Successfully Fetched'], post=post_res.to_dict())

    def Delete(self, req: account_post_pb2.AccountPostGetRequest,
               context: grpc.ServicerContext) -> account_post_pb2.AccountPostResponse:
        """
        Delete deletes a specified post
        """
        # Only need to check if Post ID exists, the user_id doesn't matter.
        # For admin purposes, the user_id can be -1 to delete any post - reducing complexity.
        # If there was a need for audit logs, then the user_id would be required.
        if req.post_id == 0:
            return account_post_pb2.AccountPostResponse(success=False, http_status=400, error_message=['Post ID is Required'])

        with get_db() as session:
            post_res = session.query(Post).filter(Post.id == req.post_id).first()

            if post_res is None:
                return account_post_pb2.AccountPostResponse(success=False, http_status=400, error_message=['Post selected does not exist'])

            if post_res.user_id != req.user_id and req.user_id != -1:
                return account_post_pb2.AccountPostResponse(success=False, http_status=400, error_message=['Post does not belong to user'])

            tag_res = session.query(PostTag).filter(PostTag.post_id == req.post_id).all()
            for tag in tag_res:
                session.delete(tag)

            session.commit()

            image_res = session.query(PostImage).filter(PostImage.post_id == req.post_id).all()

            for image in image_res:
                session.delete(image)

            session.commit()
            session.delete(post_res)
            session.commit()

            return account_post_pb2.AccountPostResponse(success=True, http_status=200, error_message=['Post Successfully Deleted'])