#!/bin/bash
# Git 훅 설정 스크립트
# 팀원들이 이 스크립트를 실행하여 Git 훅을 설정할 수 있습니다.

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Git 훅 설정 스크립트${NC}"
echo "=============================================="

# 현재 디렉토리를 프로젝트 루트로 변경
cd "$(git rev-parse --show-toplevel)"

# hooks 디렉토리 생성
mkdir -p scripts/hooks

echo -e "${GREEN}📁 Git 훅 디렉토리 확인 중...${NC}"

# pre-push 훅 설정
if [ -f "scripts/hooks/pre-push" ]; then
    cp scripts/hooks/pre-push .git/hooks/pre-push
    chmod +x .git/hooks/pre-push
    echo -e "${GREEN}✅ pre-push 훅 설정 완료${NC}"
else
    echo -e "${RED}❌ scripts/hooks/pre-push 파일을 찾을 수 없습니다.${NC}"
    exit 1
fi

# pre-commit 훅 설정 (pre-commit 프레임워크 사용)
echo -e "${BLUE}📦 pre-commit 프레임워크 설치 중...${NC}"
if command -v pre-commit &> /dev/null; then
    echo -e "${GREEN}✅ pre-commit이 이미 설치되어 있습니다.${NC}"
else
    echo -e "${YELLOW}📥 pre-commit을 설치합니다...${NC}"
    pip install pre-commit
fi

# pre-commit 훅 설치
echo -e "${BLUE}🔧 pre-commit 훅 설치 중...${NC}"
pre-commit install

echo -e "${GREEN}🎉 Git 훅 설정이 완료되었습니다!${NC}"
echo -e "${YELLOW}💡 이제 다음이 자동으로 실행됩니다:${NC}"
echo -e "${YELLOW}   - git commit 시: 코드 포맷팅 및 검증${NC}"
echo -e "${YELLOW}   - git push 시: 서버에 .env 파일 생성/업데이트${NC}"

echo -e "${BLUE}📋 설정된 훅들:${NC}"
echo -e "${BLUE}   - pre-commit: 코드 포맷팅 (Black) 및 검증${NC}"
echo -e "${BLUE}   - pre-push: 서버 .env 파일 자동 업데이트${NC}"

echo -e "${YELLOW}💡 서버 정보 설정 (선택사항):${NC}"
echo -e "${YELLOW}   export SERVER_HOST=211.44.169.71${NC}"
echo -e "${YELLOW}   export SERVER_USER=root${NC}"
echo -e "${YELLOW}   export SERVER_PATH=/root/intellius${NC}"
