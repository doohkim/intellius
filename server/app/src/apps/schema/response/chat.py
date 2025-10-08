from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ChatSessionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class ChatSessionListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chat_sessions: list[ChatSessionSchema]


# 채팅 메시지 관련 스키마
class ChatMessageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    session_id: int
    message_type: str
    content: str
    created_at: datetime


class ChatMessageListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chat_messages: list[ChatMessageSchema]
