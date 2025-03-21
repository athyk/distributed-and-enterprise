import traceback

import grpc
from backend.degree.database.database import get_db
from backend.degree.database.models import Degree
from backend.common.proto import degree_pb2_grpc, degree_pb2
from backend.common.utils import verify_string


class DegreeServicer(degree_pb2_grpc.DegreesServicer):
    def Create(self, req: degree_pb2.DegreeCreateRequest, context: grpc.ServicerContext) -> degree_pb2.DegreeCreateResponse:
        """
        Create allows the creation of a new degree.

        There is no .lower() call here just to allow for the creation of degrees with capital letters.

        Such as "Bachelor of Science in Computer Science" or "BSc in Computer Science"
        """
        degree_verify, degree_error = verify_string(req.name, 1, 24)

        if not degree_verify:
            return degree_pb2.DegreeCreateResponse(
                success=False,
                http_status=400,
                error_message=[degree_error],
            )

        try:
            with get_db() as session:
                degree = session.query(Degree).filter(Degree.name == req.name).first()

                if degree:
                    return degree_pb2.DegreeCreateResponse(
                        success=False,
                        http_status=400,
                        error_message=["Degree already exists"],
                    )

                degree = Degree(name=req.name)

                session.add(degree)
                session.commit()
                session.refresh(degree)
        except Exception:
            traceback.print_exc()
            return degree_pb2.DegreeCreateResponse(
                success=False,
                http_status=500,
                error_message=["An Unknown Error Occurred"],
            )

        return degree_pb2.DegreeCreateResponse(
            success=True,
            http_status=201,
            id=degree.id,
        )

    def Delete(self, req: degree_pb2.DegreeDeleteRequest, context: grpc.ServicerContext) -> degree_pb2.DegreeDeleteResponse:
        """
        Delete deletes a degree
        """
        if req.id == 0:
            return degree_pb2.DegreeDeleteResponse(
                success=False,
                http_status=400,
                error_message=["ID cannot be 0"],
            )

        with get_db() as session:
            degree = session.query(Degree).filter(Degree.id == req.id).first()
            if not degree:
                return degree_pb2.DegreeDeleteResponse(
                    success=False,
                    http_status=400,
                    error_message=["Degree not found"],
                )

            session.delete(degree)
            session.commit()

        return degree_pb2.DegreeDeleteResponse(
            success=True,
            http_status=200,
        )

    def Get(self, req: degree_pb2.DegreeGetRequest, context: grpc.ServicerContext) -> degree_pb2.DegreeGetResponse:
        """
        Get by id or name.
        """
        if req.id == 0 and req.name == "":
            return degree_pb2.DegreeGetResponse(
                success=False,
                http_status=400,
                error_message=["ID cannot be 0 and name cannot be empty"],
            )

        with get_db() as session:
            degree = session.query(Degree).filter(Degree.id == req.id).first()
            if not degree and len(req.name) > 0:
                degree = session.query(Degree).filter(Degree.name == req.name).first()

            if not degree:  # Both ID and name are invalid
                return degree_pb2.DegreeGetResponse(
                    success=False,
                    http_status=400,
                    error_message=["Degree not found"],
                )

        return degree_pb2.DegreeGetResponse(
            success=True,
            http_status=200,
            degree=degree.to_dict()
        )

    def List(self, req: degree_pb2.DegreeListRequest, context: grpc.ServicerContext) -> degree_pb2.DegreeListResponse:
        """
        List returns all Degrees found, allowing for partial name matching.
        """
        page = req.page if req.page >= 0 else 0
        limit = req.limit if 0 < req.limit <= 50 else 50
        offset = page * limit

        with get_db() as session:
            query = session.query(Degree).filter(Degree.name.ilike(f"%{req.name}%"))

            degrees = query.offset(offset).limit(limit).all()
            degree_list = [degree.to_dict() for degree in degrees]

        return degree_pb2.DegreeListResponse(
            success=True,
            http_status=200,
            degrees=degree_list
        )
