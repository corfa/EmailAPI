from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.create_msg import RequestCreateMessageDto
from api.response.message import ResponseMessageDto
from db.exceptions import DBUserNotExistsException, DBDataException, DBIntegrityException

from transport.sanic.endpoints import BaseEndpoint
from db.queries import message
from transport.sanic.exceptions import SanicUserNotFound, SanicDBException
from db.queries import message as message_queries


class CreateMessageEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session, token: dict, *args,
                          **kwargs) -> BaseHTTPResponse:
        request = RequestCreateMessageDto(body)

        try:
            db_message = message.create_message(session, request, token.get("uid"), request.recipient)
        except DBUserNotExistsException:
            raise SanicUserNotFound('User not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response = ResponseMessageDto(db_message)

        return await self.make_response_json(response.dump(), status=201)

    async def method_get(
            self, request: Request, body: dict, session, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        db_user = message_queries.get_messages(session, token.get("uid"))
        response_message = ResponseMessageDto(db_user, many=True)
        response_model = {'messages': response_message.dump()}

        return await self.make_response_json(status=200, body=response_model)
