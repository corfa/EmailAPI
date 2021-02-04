from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.path_user import RequestPatchUserDto
from api.response.user import ResponseUserDto
from api.response.user_data_get import ResponseUserGetDto
from db.database import DBSession
from db.exceptions import DBDataException, DBIntegrityException

from transport.sanic.endpoints import BaseEndpoint

from db.queries import user as user_queries

from transport.sanic.exceptions import SanicDBException


class GetDataUserEndpoint(BaseEndpoint):

    async def method_get(
            self, request: Request, body: dict, session: DBSession, rid: int, *args, **kwargs
    ) -> BaseHTTPResponse:

        db_user = user_queries.get_user(session=session, user_id=rid)

        response = ResponseUserGetDto(db_user)

        return await self.make_response_json(body=response.dump(), status=201)

    async def method_patch(
            self, request: Request, body: dict, session: DBSession, rid: int, *args, **kwargs
    ) -> BaseHTTPResponse:

        request_model = RequestPatchUserDto(body)

        db_user = user_queries.patch_user(session, request_model, user_id=rid)

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseUserDto(db_user)

        return await self.make_response_json(status=200, body=response_model.dump())
