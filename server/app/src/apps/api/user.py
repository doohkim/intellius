import logging
from fastapi import APIRouter, Depends, HTTPException, status

from ..repository.user import UserRepository
from ..schema.request import LoginRequest, SignUpRequest
from ..schema.response import JWTResponse, UserSchema
from ..model.user import User
from ..service.user import UserService

router = APIRouter()


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserSchema
)
async def register(
    request: SignUpRequest,
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
):

    # 1. 사용자명 중복 확인
    if user_repo.get_user_by_username(request.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # 2. 비밀번호 해싱
    hashed_password: str = user_service.hash_password(plain_password=request.password)
    logging.info(f"hashed_password: {hashed_password}")
    user: User = User.create(
        username=request.username, email=request.email, hashed_password=hashed_password
    )
    # 3. 새 사용자 생성
    user: User = user_repo.save_user(user)

    return UserSchema.model_validate(user)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=JWTResponse)
async def login(
    request: LoginRequest,
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
):
    """사용자 로그인"""
    # 사용자 인증
    user: User = user_service.authenticate_user(
        request.username, request.password, user_repo
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # JWT 토큰 생성
    access_token: str = user_service.create_jwt(user.username)
    return JWTResponse(access_token=access_token, token_type="bearer")


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def read_user(
    user_id: int,
    user_repo: UserRepository = Depends(),
):
    """특정 사용자 정보 조회"""
    user: User = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserSchema.model_validate(user)
