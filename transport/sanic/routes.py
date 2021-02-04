from typing import Tuple
from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return (
        endpoints.CreateUserEndpoint(
            config, context, uri='/user', methods=['POST'],
        ),
        endpoints.AuthUserEndpoint(
            config, context, uri='/auth', methods=['POST'],
        ),
        endpoints.GetDataUserEndpoint(
            config, context, uri='/user/<rid:int>', methods=['GET', 'PATCH'], auth_required=True,
        ),
        endpoints.CreateMessageEndpoint(
            config, context, uri='/msg', methods=['POST', 'GET'], auth_required=True,
        ),
        endpoints.ChangesMessageEndpoint(
            config, context, uri='/msg/<mid:int>', methods=['PATCH', 'DELETE', 'GET'], auth_required=True,
        )
    )
