#!/bin/bash
# 서버 배포 스크립트
# git pull → deploy-env.sh → docker compose up -d 실행

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 서버 배포 스크립트 시작${NC}"
echo "=============================================="

# 1. Git pull
echo -e "${GREEN}📥 Git pull 실행 중...${NC}"
git pull origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Git pull 완료${NC}"
else
    echo -e "${RED}❌ Git pull 실패${NC}"
    exit 1
fi

# 2. 환경변수 파일 생성 (deploy-env.sh 실행)
echo -e "${BLUE}🔧 환경변수 파일 생성 중...${NC}"
python3 scripts/deploy-env.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 환경변수 파일 생성 완료${NC}"
else
    echo -e "${RED}❌ 환경변수 파일 생성 실패${NC}"
    exit 1
fi

# 5. Docker Compose 실행
echo -e "${GREEN}🐳 Docker Compose 실행 중...${NC}"
docker-compose --env-file=./.deploy/production/.env --profile=production up --build --force-recreate -d

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Docker Compose 실행 완료${NC}"
else
    echo -e "${RED}❌ Docker Compose 실행 실패${NC}"
    exit 1
fi

# 6. 상태 확인
echo -e "${BLUE}📊 컨테이너 상태 확인...${NC}"
docker-compose ps

echo -e "${GREEN}🎉 서버 배포 완료!${NC}"
echo -e "${YELLOW}💡 로그 확인: docker-compose logs -f${NC}"
