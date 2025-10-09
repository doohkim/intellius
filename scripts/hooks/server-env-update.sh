#!/bin/bash
# Pre-push 훅: 서버 .env 파일 업데이트 스크립트

echo "🚀 Pre-push 훅 실행 중..."
echo "📡 서버에 연결하여 .env 파일을 생성/업데이트합니다..."

# 서버 정보 (환경변수에서 가져오거나 기본값 사용)
SERVER_HOST=${SERVER_HOST:-"211.44.169.71"}
SERVER_USER=${SERVER_USER:-"root"}

# SSH로 서버에 연결하여 .env 파일 생성/업데이트
ssh -o StrictHostKeyChecking=no -p 23231 $SERVER_USER@$SERVER_HOST << 'EOF'
    echo "🔐 서버에서 .env 파일 생성 중..."
    
    # .deploy/production 디렉토리 생성
    mkdir -p .deploy/production
    
    # .env 파일이 없으면 생성
    if [ ! -f .deploy/production/.env ]; then
        echo "📝 .env 파일을 생성합니다..."
        touch .deploy/production/.env
        echo "# Production Environment Variables" > .deploy/production/.env
        echo "# Generated on $(date)" >> .deploy/production/.env
        echo "✅ .env 파일이 생성되었습니다."
    else
        echo "📝 기존 .env 파일을 업데이트합니다..."
        echo "# Updated on $(date)" >> .deploy/production/.env
        echo "✅ .env 파일이 업데이트되었습니다."
    fi
    
    echo "📁 파일 위치: $(pwd)/.deploy/production/.env"
    echo "📊 파일 크기: $(wc -l < .deploy/production/.env) lines"
EOF

if [ $? -eq 0 ]; then
    echo "✅ 서버의 .env 파일 생성/업데이트가 완료되었습니다."
    echo "🎉 Pre-push 훅이 성공적으로 완료되었습니다."
else
    echo "❌ 서버 연결 또는 .env 파일 생성에 실패했습니다."
    echo "💡 다음을 확인하세요:"
    echo "   - SSH 키가 서버에 등록되어 있는지"
    echo "   - SERVER_HOST, SERVER_USER 환경변수가 올바른지"
    echo "   - 서버가 접근 가능한지"
    exit 1
fi
