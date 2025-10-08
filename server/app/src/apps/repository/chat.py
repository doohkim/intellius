"""
AI 상담 채팅 Repository
====================

데이터베이스 쿼리 로직을 담당하는 Repository 레이어
- ChatSession 관련 CRUD 작업
- ChatMessage 관련 CRUD 작업
- 사용자별 데이터 격리 보장
"""

from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from ...core.database.connection import get_db
from ..model.chat import ChatSession, ChatMessage
from ..model.user import User


class ChatRepository:
    """AI 상담 채팅 데이터 Repository"""

    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_user_sessions(self, user_id: int) -> List[ChatSession]:
        """사용자의 모든 AI 상담 세션 조회 (최신 순)"""
        return (
            self.session.query(ChatSession)
            .filter(ChatSession.user_id == user_id)
            .order_by(ChatSession.created_at.desc())
            .all()
        )

    def get_session_by_id(self, session_id: int, user_id: int) -> Optional[ChatSession]:
        """특정 상담 세션 조회 (소유권 확인)"""
        return (
            self.session.query(ChatSession)
            .filter(ChatSession.id == session_id, ChatSession.user_id == user_id)
            .first()
        )

    def get_session_messages(self, session_id: int) -> List[ChatMessage]:
        """특정 상담 세션의 모든 메시지 조회 (시간 순)"""
        return (
            self.session.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )

    def create_session(self, session: ChatSession) -> ChatSession:
        """새로운 상담 세션 생성"""
        self.session.add(instance=session)
        self.session.commit()
        self.session.refresh(instance=session)
        return session

    def create_message(self, message: ChatMessage) -> ChatMessage:
        """새로운 메시지 생성"""
        self.session.add(instance=message)
        self.session.commit()
        self.session.refresh(instance=message)
        return message

    def delete_session(self, session: ChatSession) -> bool:
        """상담 세션 삭제 (관련 메시지도 함께 삭제)"""
        # 세션 소유권 확인
        session = self.get_session_by_id(session_id=session.id, user_id=session.user_id)
        if not session:
            return False

        # 관련 메시지들 삭제
        self.session.query(ChatMessage).filter(
            ChatMessage.session_id == session.id
        ).delete()
        # 세션 삭제
        self.session.delete(instance=session)
        self.session.commit()
        return True
