# Intellius Chat Service

## 정적 파일 구조

- `css/` - 스타일시트 파일
- `js/` - JavaScript 파일  
- `images/` - 이미지 파일
- `docs/` - 문서 파일

## 사용법

1. 서버 실행: `uvicorn src.main:app --reload`
2. 정적 파일 브라우저: `http://localhost:8000/static-files`
3. 개별 파일 접근: `http://localhost:8000/static/파일경로`
