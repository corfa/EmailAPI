from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.auth_user import RequestAuthUserDto
from api.response.auth_user import AuthResponseObject
from api.response.auth_user import ResponseAuthUserDto
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFound, SanicAuthException

from db.queries import user as user_queries
from db.exceptions import DBUserNotExistsException

from helpers.password import check_hash, CheckPasswordHashException

from helpers.auth import create_token


class AuthUserEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestAuthUserDto(body)

        try:
            db_user = user_queries.get_user(session, login=request_model.login)
        except DBUserNotExistsException:
            raise SanicUserNotFound('User not found')

        try:
            check_hash(request_model.password, db_user.password)
        except CheckPasswordHashException:
            raise SanicAuthException('Wrong password')

        payload = {
            'uid': db_user.id,
        }

        token = create_token(payload)
        response = AuthResponseObject(token)
        response_model = ResponseAuthUserDto(response)

        return await self.make_response_json(
            body=response_model.dump(),
            status=200,
        )
