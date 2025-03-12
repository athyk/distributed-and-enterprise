import traceback
from datetime import datetime, UTC

import grpc
from backend.tag.database.database import get_db
from backend.tag.database.models import Tag
from backend.common.proto import tag_pb2_grpc, tag_pb2
from backend.common.utils import verify_string


class TagServicer(tag_pb2_grpc.TagsServicer):
    def Create(self, req: tag_pb2.TagCreateRequest, context: grpc.ServicerContext) -> tag_pb2.TagCreateResponse:
        """
        Create allows the creation of a new tag or increments the count of an existing tag.

        It's both a POST and PUT request.
        """
        tag_verify, tag_error = verify_string(req.name, 1, 24)

        if not tag_verify and req.id == 0:
            return tag_pb2.TagCreateResponse(
                success=False,
                http_status=400,
                error_message=["Tag name must be between 1 and 24 characters. Or ID must be greater than 0"],
            )

        req.name = req.name.lower()
        try:
            with get_db() as session:
                if req.name != "":
                    tag = session.query(Tag).filter(Tag.name == req.name).first()

                    if not tag:
                        tag = Tag(name=req.name)

                    tag.count += 1
                    tag.updated_at = datetime.now(UTC)
                    session.add(tag)
                    session.commit()
                    session.refresh(tag)
                else:
                    tag = session.query(Tag).filter(Tag.id == req.id).first()
                    if not tag:
                        return tag_pb2.TagCreateResponse(
                            success=False,
                            http_status=400,
                            error_message=["Tag not found"],
                        )
                    tag.count += 1
                    tag.updated_at = datetime.now(UTC)
                    session.add(tag)
                    session.commit()
                    session.refresh(tag)
        except Exception:
            traceback.print_exc()
            return tag_pb2.TagCreateResponse(
                success=False,
                http_status=500,
                error_message=["An Unknown Error Occurred"],
            )

        return tag_pb2.TagCreateResponse(
            success=True,
            http_status=201,
            id=tag.id,
        )

    def Delete(self, req: tag_pb2.TagDeleteRequest, context: grpc.ServicerContext) -> tag_pb2.TagDeleteResponse:
        """
        Delete deletes a tag
        """
        if req.id == 0:
            return tag_pb2.TagDeleteResponse(
                success=False,
                http_status=400,
                error_message=["ID cannot be 0"],
            )

        with get_db() as session:
            tag = session.query(Tag).filter(Tag.id == req.id).first()
            if not tag:
                return tag_pb2.TagDeleteResponse(
                    success=False,
                    http_status=400,
                    error_message=["Tag not found"],
                )

            session.delete(tag)
            session.commit()

        return tag_pb2.TagDeleteResponse(
            success=True,
            http_status=200,
        )

    def Get(self, req: tag_pb2.TagGetRequest, context: grpc.ServicerContext) -> tag_pb2.TagGetResponse:
        """
        Get by id or name.
        """
        if req.id == 0 and req.name == "":
            return tag_pb2.TagGetResponse(
                success=False,
                http_status=400,
                error_message=["ID cannot be 0 and name cannot be empty"],
            )

        with get_db() as session:
            tag = session.query(Tag).filter(Tag.id == req.id).first()
            if not tag and len(req.name) > 0:
                req.name = req.name.lower()
                tag = session.query(Tag).filter(Tag.name == req.name).first()

            if not tag:  # Both ID and name are invalid
                return tag_pb2.TagGetResponse(
                    success=False,
                    http_status=400,
                    error_message=["Tag not found"],
                )

        return tag_pb2.TagGetResponse(
            success=True,
            http_status=200,
            tag=tag.to_dict()
        )

    def List(self, req: tag_pb2.TagListRequest, context: grpc.ServicerContext) -> tag_pb2.TagListResponse:
        """
        List returns all tags found, allowing for partial name matching.
        """
        page = req.page if req.page >= 0 else 0
        limit = req.limit if 0 < req.limit <= 50 else 50
        offset = page * limit

        with get_db() as session:
            query = session.query(Tag)

            if req.name:
                req.name = req.name.lower()
                query = query.filter(Tag.name.ilike(f"%{req.name}%"))

            tags = query.order_by(Tag.count.desc()).offset(offset).limit(limit).all()
            tag_list = [tag.to_dict() for tag in tags]

        return tag_pb2.TagListResponse(
            success=True,
            http_status=200,
            tags=tag_list
        )
