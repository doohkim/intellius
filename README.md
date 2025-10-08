# Intellius Chat Service

10만 명의 회원을 대상으로 하는 상담 채팅 서비스 API입니다.

## 기능

- **사용자 인증**: 회원가입, 로그인, JWT 토큰 기반 인증
- **채팅 세션 관리**: 채팅 세션 생성, 조회, 삭제
- **AI 채팅 응답**: 더미 AI 응답 (1-3초 랜덤 지연)
- **채팅 메시지 관리**: 메시지 전송, 대화 기록 조회

## 기술 스택

- **Backend**: FastAPI (Python 3.13+)
- **Database**: MariaDB
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **Password Hashing**: bcrypt

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -e .
```

### 2. 데이터베이스 설정

MariaDB

```
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/intellius_chat
```

### 4. 서버 실행
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

서버가 실행되면 `http://localhost:8000`에서 API에 접근할 수 있습니다.

## API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API 엔드포인트


### 사용자 (Users)

### 사용자 관리
- `POST /api/api/users/register` - 회원가입
- `POST /api/api/users/login` - 로그인
- `GET /api/api/users/{user_id}` - 사용자 정보 조회

### 채팅 (Chat)

- `GET /api/api/chat/sessions` - 채팅 세션 목록 조회
- `GET /api/api/chat/sessions/{session_id}/messages` - 세션 메시지 조회
- `POST /api/api/chat/sessions/{session_id}/messages` - 메시지 전송
- `DELETE /api/api/chat/sessions/{session_id}` - 세션 삭제

## 사용 예시

### 1. 회원가입

```bash
curl -X POST "http://localhost:8000/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123"
  }'
```

### 2. 로그인

```bash
curl -X POST "http://localhost:8000/api/users/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```
### 3. 채팅 세션 목록 조회

```bash
curl -X GET "http://localhost:8000/api/api/chat/sessions" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
### 4. 채팅 메시지 전송

```bash
curl -X POST "http://localhost:8000/api/api/chat/sessions/1/messages" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "안녕하세요, 도움이 필요합니다.",
    "message_type": "user"
  }'
```
### 5. 세션 메시지 조회

```bash
curl -X GET "http://localhost:8000/api/api/chat/sessions/1/messages" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🗄️ 데이터베이스 스키마

### Users 테이블
- `id`: 사용자 ID (Primary Key)
- `email`: 이메일 (Unique)
- `username`: 사용자명 (Unique)
- `hashed_password`: 해싱된 비밀번호
- `is_active`: 활성 상태
- `created_at`: 생성일시
- `updated_at`: 수정일시

### ChatSessions 테이블
- `id`: 세션 ID (Primary Key)
- `user_id`: 사용자 ID (Foreign Key)
- `title`: 세션 제목 (Nullable)
- `created_at`: 생성일시
- `updated_at`: 수정일시

### ChatMessages 테이블
- `id`: 메시지 ID (Primary Key)
- `user_id`: 사용자 ID (Foreign Key)
- `session_id`: 세션 ID (Foreign Key)
- `message_type`: 메시지 타입 ('user' 또는 'ai')
- `content`: 메시지 내용
- `created_at`: 생성일시
## 개발 환경 설정

### 코드 스타일

이 프로젝트는 다음 코딩 스타일을 따릅니다:

- **PEP 8**: Python 코드 스타일 가이드
- **Type Hints**: 모든 함수에 타입 힌트 적용
- **Docstrings**: 모든 함수에 독스트링 작성
- **Error Handling**: 적절한 예외 처리 및 HTTP 상태 코드 사용

### 테스트

```bash
# 테스트 실행 (추후 구현 예정)
pytest
```

## 배포

### Docker (추후 구현 예정)

```bash
# Docker 이미지 빌드
docker build -t intellius-chat .

# 컨테이너 실행
docker run -p 8000:8000 intellius-chat
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
