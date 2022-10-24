from datetime import datetime

from sqlalchemy.dialects.postgresql import TEXT
from sqlmodel import Column, Enum, Field, SQLModel

from app.db.enums import NotificationType


__all__ = [
    'User',
    'Notification',
]


class BaseModel(SQLModel):
    id: int = Field(default=None, primary_key=True)


class User(BaseModel, table=True):
    token: str = Field(index=True)


class Notification(BaseModel, table=True):
    user_id: int = Field(default=None, foreign_key='user.id')
    sender_name: str
    type: NotificationType = Field(sa_column=Column(Enum(NotificationType)))
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    text: str = Field(sa_column=Column(TEXT))
    viewed: bool = False
