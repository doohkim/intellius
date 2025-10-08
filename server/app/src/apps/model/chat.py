from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..schema.request.chat import ChatSessionRequest, ChatMessageRequest

from ...core.model import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 관계 설정
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session")

    def __repr__(self):
        return f"ChatSession(id={self.id}, user_id={self.user_id}, title={self.title})"

    @classmethod
    def create(cls, user_id: int, title: str) -> "ChatSession":
        return cls(user_id=user_id, title=title)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    message_type = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    session = relationship("ChatSession", back_populates="messages")
    user = relationship("User")

    @classmethod
    def create(
        cls, user_id: int, session_id: int, message_type: str, content: str
    ) -> "ChatMessage":
        return cls(
            session_id=session_id,
            user_id=user_id,
            message_type=message_type,
            content=content,
        )
