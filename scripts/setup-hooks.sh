#!/bin/bash

# =============================================================================
# 서버에서 Git 훅 설정 스크립트
# =============================================================================

echo "🔧 서버 Git 훅 설정 중..."

# post-merge 훅 설정
if [ -f "scripts/hooks/post-merge" ]; then
    cp scripts/hooks/post-merge .git/hooks/post-merge
    chmod +x .git/hooks/post-merge
    echo "✅ post-merge 훅 설정 완료"
else
    echo "❌ scripts/hooks/post-merge 파일을 찾을 수 없습니다."
    exit 1
fi

echo "🎉 Git 훅 설정이 완료되었습니다!"
echo "💡 이제 git pull할 때마다 환경변수 파일이 자동으로 생성됩니다."
