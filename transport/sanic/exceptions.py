from sanic.exceptions import SanicException


class SanicResponseForbiddenException(SanicException):
    status_code = 403


class SanicRequestValidationException(SanicException):
    status_code = 400


class SanicEmployeeConflictException(SanicException):
    status_code = 409


class SanicResponseValidationException(SanicException):
    status_code = 500


class SanicPasswordHashException(SanicException):
    status_code = 500


class SanicDBException(SanicException):
    status_code = 500


class SanicAuthException(SanicException):
    status_code = 401


class SanicUserNotFound(SanicException):
    status_code = 404
