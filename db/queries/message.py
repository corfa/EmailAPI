from typing import List

from api.request.create_msg import RequestCreateMessageDto
from api.request.path_msg import RequestPatchMessageDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException,  DBMessageNotExistsException
from db.models import DBMessage


def create_message(session: DBSession, message: RequestCreateMessageDto, uid: int, recipient: str) -> DBMessage:
    if session.get_user_by_login(recipient) is None:
        raise DBUserNotExistsException
    new_message = DBMessage(
        message=message.message,
        sender_id=uid,
        recipient_id=session.get_user_by_login(recipient).id
    )
    session.add_model(new_message)

    return new_message


def get_messages(session: DBSession, uid: int) -> List['DBMessage']:
    return session.get_messages_all(uid)


def get_message(session: DBSession, mid: int, uid: int) -> DBMessage:
    db_message = session.get_message_by_id_for_get(mid, uid)
    if db_message is None:
        raise DBMessageNotExistsException
    return db_message


def patch_message(session: DBSession, message: RequestPatchMessageDto, mid: int, uid: int) -> DBMessage:

    db_message = session.get_message_by_id_for_changes(mid, uid)
    if db_message is None:
        raise DBMessageNotExistsException

    for attr in message.fields:
        if hasattr(message, attr):
            value = getattr(message, attr)
            setattr(db_message, attr, value)

    return db_message


def delete_message(session: DBSession, mid: int, uid: int) -> DBMessage:
    db_message = session.get_message_by_id_for_changes(mid, uid)
    if db_message is None:
        raise DBMessageNotExistsException
    db_message.is_delete = True
    return db_message
