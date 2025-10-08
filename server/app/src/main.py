import logging
from tracemalloc import Statistic
import redis
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

from .core.model import Base
from .apps.router import api_router as api_router_v1
from .core.database.connection import engine
from .core.secrets import load_secrets_to_env, get_secret_value

# AWS Secrets Manager에서 시크릿 로드
try:
    # 환경변수에서 시크릿 이름 가져오기 (기본값: intellius-secrets)
    secret_name = os.getenv("SECRET_NAME", None)
    if not secret_name:
        print("❌ SECRET_NAME 환경변수가 설정되지 않았습니다.")
        raise Exception("❌ SECRET_NAME 환경변수가 설정되지 않았습니다.")
    print(f"시크릿 '{secret_name}'에서 환경변수 로드 시작")
    load_secrets_to_env(secret_name)
    print(f"시크릿 '{secret_name}'에서 환경변수 로드 완료")
except Exception as e:
    print(f"시크릿 로드 실패: {e}")
    print("로컬 환경변수 또는 .env 파일을 사용합니다.")

# 데이터베이스 테이블 생성
try:
    Base.metadata.create_all(bind=engine)
    print("데이터베이스 테이블 생성 완료")
except Exception as e:
    print(f"데이터베이스 연결 실패: {e}")
    print("Docker Compose로 데이터베이스 실행: docker-compose up -d database")

app = FastAPI(title="Intellius Chat Service API", version="1.0.0", debug=True)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8000",
        "https://localhost:3000",
        "https://localhost:8080",
        "https://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Intellius Chat Service API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/secrets/test")
async def test_secrets():
    """시크릿 테스트 엔드포인트 (개발용)"""
    try:
        secret_name = os.getenv("SECRET_NAME", None)
        if not secret_name:
            print("❌ SECRET_NAME 환경변수가 설정되지 않았습니다.")
            raise Exception("❌ SECRET_NAME 환경변수가 설정되지 않았습니다.")
        print(f"시크릿 '{secret_name}'에서 환경변수 로드 시작")
        from .core.secrets import get_secret

        # 시크릿에서 모든 키 가져오기 (값은 마스킹)
        secrets = get_secret(secret_name)
        masked_secrets = {}
        for key, value in secrets.items():
            # 값의 일부만 보여주기 (보안을 위해)
            if isinstance(value, str) and len(value) > 4:
                masked_secrets[key] = value[:2] + "*" * (len(value) - 4) + value[-2:]
            else:
                masked_secrets[key] = "***"

        return {
            "status": "success",
            "secret_name": secret_name,
            "keys": list(secrets.keys()),
            "masked_values": masked_secrets,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# 템플릿 설정
templates = Jinja2Templates(directory="templates")


# 정적 파일 확인 페이지
@app.get("/static-files", response_class=HTMLResponse)
async def static_files_browser(request: Request):
    static_dir = "static"
    files = []

    if os.path.exists(static_dir):
        for root, dirs, filenames in os.walk(static_dir):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, static_dir)
                files.append(
                    {
                        "name": filename,
                        "path": relative_path,
                        "url": f"/static/{relative_path}",
                    }
                )

    return templates.TemplateResponse(
        "static_browser.html", {"request": request, "files": files}
    )


# 정적 파일 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

# template
templates = Jinja2Templates(directory="templates")

# router
app.include_router(api_router_v1, prefix="/api")
