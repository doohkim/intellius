from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# 채팅 세션 관련 스키마
class ChatSessionRequest(BaseModel):
    user_id: int
    title: Optional[str] = None


# 채팅 요청/응답 스키마
class ChatMessageRequest(BaseModel):
    user_id: int
    session_id: Optional[int] = None
    message_type: str
    content: str
