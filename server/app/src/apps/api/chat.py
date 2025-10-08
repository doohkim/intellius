"""
AI 상담 채팅 서비스 API
====================

AI 상담 서비스 플로우:
1. 사용자 인증 (JWT 토큰 검증)
2. 상담 메시지 전송 시 자동으로 상담방 생성
3. AI 상담 응답 (더미 데이터, 1-3초 지연)
4. 상담 세션 조회/관리
5. 상담 세션 삭제

API 엔드포인트:
- POST /send: 상담 메시지 전송 및 AI 응답 (핵심 - 상담방 자동 생성)
- GET /sessions: 사용자의 상담 세션 목록 조회
- GET /sessions/{id}/messages: 특정 상담 세션의 메시지 목록 조회
- DELETE /sessions/{id}: 상담 세션 삭제

AI 상담 UX:
- 첫 상담 메시지 전송 → 상담방 자동 생성
- 상담 메시지 전송 → AI 상담사 응답 (1-3초 지연)
- 상담방 목록에서 상담 이어가기
"""

import random
import asyncio
from datetime import datetime

from ..model.user import User
from ..model.chat import ChatSession, ChatMessage
from ..repository.user import UserRepository
from ..repository.chat import ChatRepository
from ..schema import ChatMessageRequest
from ..schema.response.chat import (
    ChatMessageSchema,
    ChatSessionListSchema,
    ChatSessionSchema,
    ChatMessageListSchema,
)
from ..service.user import UserService
from ...security import get_access_token

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()

# AI 상담사 더미 응답 데이터 (1-3초 랜덤 지연으로 실제 상담사처럼 동작)
AI_COUNSELOR_RESPONSES = [
    "안녕하세요! 무엇을 도와드릴까요?",
    "좋은 질문이네요. 좀 더 자세히 설명해주시겠어요?",
    "이해했습니다. 그런 상황이시군요.",
    "제가 도울 수 있는 방법이 있을 것 같습니다.",
    "흥미로운 관점이네요. 다른 각도에서 생각해보면 어떨까요?",
    "그런 고민이 있으시는군요. 함께 해결책을 찾아보겠습니다.",
    "좋은 아이디어입니다! 더 구체적으로 계획을 세워보시는 것은 어떨까요?",
    "이해하기 어려운 부분이 있으시다면 언제든 말씀해주세요.",
    "그런 상황에서는 이런 방법도 고려해볼 수 있습니다.",
    "정말 좋은 질문입니다. 이에 대해 자세히 설명드리겠습니다.",
]

# POST /sessions 엔드포인트 제거
# AI 상담 서비스처럼 상담 메시지 전송 시 자동으로 상담방 생성


@router.get(
    "/sessions", status_code=status.HTTP_200_OK, response_model=ChatSessionListSchema
)
async def get_chat_sessions(
    access_token: str = Depends(get_access_token),
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
    chat_repo: ChatRepository = Depends(),
) -> ChatSessionListSchema:
    """
    2단계: 사용자의 AI 상담 세션 목록 조회
    ===================================
    - 현재 로그인한 사용자의 모든 AI 상담 세션 목록 반환
    - 최신 순으로 정렬 (created_at desc)
    - 사용자별로 격리된 상담 데이터만 조회 (보안)
    """
    # 사용자 정보 조회
    username: str = user_service.decode_jwt(access_token=access_token)
    user: User = user_repo.get_user_by_username(username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    sessions: list[ChatSession] = chat_repo.get_user_sessions(user_id=user.id)

    # SQLAlchemy 모델을 Pydantic 스키마로 변환
    chat_sessions = [ChatSessionSchema.model_validate(session) for session in sessions]
    return ChatSessionListSchema(chat_sessions=chat_sessions)


@router.get(
    "/sessions/{session_id}/messages",
    status_code=status.HTTP_200_OK,
    response_model=ChatMessageListSchema,
)
async def get_chat_messages(
    session_id: int,
    access_token: str = Depends(get_access_token),
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
    chat_repo: ChatRepository = Depends(),
) -> ChatMessageListSchema:
    """
    3단계: 특정 AI 상담 세션의 메시지 목록 조회
    =========================================
    - 특정 AI 상담 세션의 모든 상담 메시지 조회
    - 상담 세션 소유권 확인 (보안)
    - 시간 순으로 정렬 (오래된 상담 메시지부터)
    """
    # 사용자 정보 조회
    username: str = user_service.decode_jwt(access_token=access_token)
    user: User = user_repo.get_user_by_username(username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # 상담 세션 소유권 확인 (보안 검증)
    session = chat_repo.get_session_by_id(session_id, user.id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI counseling session not found",
        )
    # Repository를 통한 메시지 조회 (시간 순)
    messages = chat_repo.get_session_messages(session_id)

    # SQLAlchemy 모델을 Pydantic 스키마로 변환 (빈 배열도 처리)
    chat_messages = [ChatMessageSchema.model_validate(message) for message in messages]
    return ChatMessageListSchema(chat_messages=chat_messages)


@router.post("/send", status_code=status.HTTP_200_OK, response_model=ChatMessageSchema)
async def send_message(
    request: ChatMessageRequest,
    access_token: str = Depends(get_access_token),
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
    chat_repo: ChatRepository = Depends(),
):
    """
    AI 상담 메시지 전송 및 AI 상담사 응답
    ================================================

    AI 상담 서비스 UX 구현:
    - 첫 상담 메시지 전송 → 상담방 자동 생성
    - 상담 메시지 전송 → AI 상담사 응답 (1-3초 지연)
    - 상담방 목록에서 상담 이어가기

    플로우:
    1. 상담 세션 확인/자동 생성 (AI 상담 스타일)
    2. 사용자 상담 메시지 저장
    3. AI 상담사 응답 생성 (지연)
    4. AI 상담사 응답 저장
    5. 상담 응답 반환
    """

    # 사용자 정보 조회
    username: str = user_service.decode_jwt(access_token=access_token)
    user: User = user_repo.get_user_by_username(username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # 1. 상담 세션 확인 또는 자동 생성 (AI 상담 스타일)
    if request.session_id:
        # 기존 상담방 사용
        session: ChatSession = chat_repo.get_session_by_id(request.session_id, user.id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AI counseling session not found",
            )
    else:
        # 🚀 AI 상담 서비스처럼 첫 상담 메시지 전송 시 상담방 자동 생성
        session: ChatSession = ChatSession.create(
            user_id=user.id, title=f"채팅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        session: ChatSession = chat_repo.create_session(session=session)

    # 2. 사용자 상담 메시지 저장
    user_message: ChatMessage = ChatMessage.create(
        user_id=user.id,
        session_id=session.id,
        message_type=request.message_type,
        content=request.content,
    )
    user_message: ChatMessage = chat_repo.create_message(message=user_message)
    # 3. AI 상담사 응답 생성 (1-3초 랜덤 지연으로 실제 상담사처럼 동작)
    delay = random.uniform(1.0, 3.0)
    await asyncio.sleep(delay)

    # AI의 응답 가능은 실제 AI를 사용하지 말고 임의의 더미 데이터를 답변.
    ai_response = random.choice(AI_COUNSELOR_RESPONSES)

    # 4. AI 상담사 응답 메시지 저장
    ai_message: ChatMessage = ChatMessage.create(
        user_id=user.id,
        session_id=session.id,
        message_type="assistant",
        content=ai_response,
    )
    ai_message: ChatMessage = chat_repo.create_message(message=ai_message)

    # 5. 상담 응답 반환
    return ChatMessageSchema(
        id=ai_message.id,
        user_id=user.id,
        session_id=session.id,
        message_type="assistant",
        content=ai_response,
        created_at=ai_message.created_at,
    )
