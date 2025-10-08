# 서버 설정 가이드

## 🚀 서버에서 환경변수 자동 생성 설정

### 1. 서버에 프로젝트 클론
```bash
git clone https://github.com/doohkim/intellius.git
cd intellius
```

### 2. 환경변수 설정
```bash
export SECRET_NAME=prod/intellius
export AWS_ACCESS_KEY_ID=your_aws_access_key
export AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

### 3. Git 훅 설정
```bash
# Git 훅 설정 스크립트 실행
./scripts/setup-hooks.sh
```

### 4. 테스트
```bash
# Git pull 시뮬레이션 (환경변수 파일 자동 생성)
git pull origin main
```

## ✅ 완료!

이제 서버에서 `git pull`할 때마다:
1. AWS Secrets Manager에서 시크릿 자동 로드
2. `.deploy/production/.env` 파일 자동 생성/업데이트
3. 모든 환경변수가 서버에 설정됨

## 🔧 환경변수 파일 위치
- `.deploy/production/.env` - 자동 생성되는 환경변수 파일
- 이 파일은 git에 추적되지 않음
