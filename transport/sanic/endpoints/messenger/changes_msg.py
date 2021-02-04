from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.path_msg import RequestPatchMessageDto
from api.response.message import ResponseMessageDto
from db.exceptions import DBDataException, DBIntegrityException, DBMessagesNoAccess, DBMessageNotExistsException

from transport.sanic.endpoints import BaseEndpoint

from transport.sanic.exceptions import SanicDBException, SanicResponseForbiddenException
from db.queries import message as message_queries


class ChangesMessageEndpoint(BaseEndpoint):
    async def method_patch(
            self, request: Request, body: dict, session, mid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        request_model = RequestPatchMessageDto(body)

        try:
            db_message = message_queries.patch_message(session, request_model, mid=mid, uid=token.get("uid"))
        except (DBMessagesNoAccess, DBMessageNotExistsException):
            raise SanicResponseForbiddenException('message not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_delete(
            self, request: Request, body: dict, session, mid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        try:
            message_queries.delete_message(session, mid, uid=token.get("uid"))
        except (DBMessagesNoAccess, DBMessageNotExistsException):
            raise SanicResponseForbiddenException('message not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)

    async def method_get(
            self, request: Request, body: dict, session, mid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        try:
            db_message = message_queries.get_message(session, mid, uid=token.get("uid"))
        except (DBMessagesNoAccess, DBMessageNotExistsException):
            raise SanicResponseForbiddenException('message not found')
        response_model = ResponseMessageDto(db_message)
        return await self.make_response_json(status=200, body=response_model.dump())
