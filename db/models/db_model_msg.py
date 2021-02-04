from sqlalchemy import Column, VARCHAR,  BOOLEAN, Integer, ForeignKey

from db.models import BaseModel


class DBMessage(BaseModel):

    __tablename__ = 'messages'
    message = Column(VARCHAR(50))
    is_delete = Column(BOOLEAN(), nullable=False, default=False)
    sender_id = Column(Integer, ForeignKey('users.id'))
    recipient_id = Column(Integer, ForeignKey('users.id'))