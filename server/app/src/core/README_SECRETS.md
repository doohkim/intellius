# AWS Secrets Manager 사용법

## 1. AWS Secrets Manager에서 시크릿 생성

### AWS 콘솔에서 시크릿 생성
1. AWS Secrets Manager 콘솔에 접속
2. "새 보안 암호 저장" 클릭
3. **보안 암호 유형**: "다른 유형의 보안 암호" 선택
4. **키/값 페어**: "키/값" 탭 선택
5. JSON 형태로 키-값 쌍 입력:

```json
{
  "DATABASE_URL": "mysql://user:password@localhost:3306/dbname",
  "REDIS_URL": "redis://localhost:6379",
  "SECRET_KEY": "your-secret-key-here",
  "AWS_ACCESS_KEY_ID": "your-aws-access-key",
  "AWS_SECRET_ACCESS_KEY": "your-aws-secret-key",
  "MYSQL_ROOT_PASSWORD": "your-mysql-password",
  "MYSQL_DATABASE": "intellius_db",
  "MYSQL_USER": "intellius_user",
  "MYSQL_PASSWORD": "your-mysql-user-password"
}
```

6. **암호화 키**: "aws/secretsmanager" 선택
7. 시크릿 이름: `intellius-secrets` (또는 원하는 이름)
8. 설명 입력 후 생성

## 2. AWS 자격 증명 설정

### 방법 1: AWS CLI 설정
```bash
aws configure
```

### 방법 2: 환경변수 설정
```bash
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_DEFAULT_REGION=ap-northeast-2
```

### 방법 3: IAM 역할 사용 (EC2/ECS에서)
- EC2 인스턴스에 IAM 역할 연결
- ECS 태스크에 IAM 역할 연결

## 3. 애플리케이션에서 사용

### 자동 로드 (권장)
애플리케이션 시작 시 자동으로 시크릿을 환경변수로 로드합니다.

```python
# main.py에서 자동으로 실행됨
load_secrets_to_env("intellius-secrets")
```

### 수동 사용
```python
from src.core.secrets import get_secret, get_secret_value

# 전체 시크릿 가져오기
secrets = get_secret("intellius-secrets")
database_url = secrets["DATABASE_URL"]

# 특정 값만 가져오기
database_url = get_secret_value("intellius-secrets", "DATABASE_URL")
```

## 4. 환경변수 설정

### ⚠️ 보안 주의사항
- `.env` 파일은 **절대 공개 저장소에 올리지 마세요**
- `.gitignore`에 `.env`가 포함되어 있는지 확인하세요
- 실제 AWS 자격증명은 안전하게 보관하세요

### .env 파일 생성
```bash
# 프로젝트 루트에 .env 파일 생성
touch .env
```

### .env 파일 내용
```bash
# AWS Secrets Manager 설정
SECRET_NAME=secret_name
AWS_DEFAULT_REGION=ap-northeast-2
AWS_ACCESS_KEY_ID=your-actual-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-actual-aws-secret-access-key

# 애플리케이션 설정
WORKER_TYPE=async
GUNICORN_WORKERS=9
GUNICORN_THREADS=2

# DDNS Route53 설정
AWS_HOSTED_ZONE_ID=your-hosted-zone-id
DOMAINS=your-domain.com
```

## 5. 테스트

### 시크릿 연결 테스트
```bash
curl http://localhost:8000/secrets/test
```

### 응답 예시
```json
{
  "status": "success",
  "secret_name": "intellius-secrets",
  "keys": ["DATABASE_URL", "REDIS_URL", "SECRET_KEY"],
  "masked_values": {
    "DATABASE_URL": "my***db",
    "REDIS_URL": "re***79",
    "SECRET_KEY": "se***ey"
  }
}
```

## 6. 보안 고려사항

1. **IAM 권한**: 최소 권한 원칙 적용
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "secretsmanager:GetSecretValue"
         ],
         "Resource": "arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:intellius-secrets-*"
       }
     ]
   }
   ```

2. **로깅**: 시크릿 값은 로그에 출력하지 않음
3. **에러 처리**: 시크릿 로드 실패 시 로컬 환경변수 사용
4. **암호화**: KMS 키를 사용한 추가 암호화 권장

## 7. 문제 해결

### 자격 증명 오류
```
NoCredentialsError: AWS 자격 증명을 찾을 수 없습니다
```
→ AWS CLI 설정 또는 환경변수 확인

### 시크릿을 찾을 수 없음
```
ResourceNotFoundException: 시크릿을 찾을 수 없습니다
```
→ 시크릿 이름과 리전 확인

### 권한 부족
```
AccessDeniedException: 액세스가 거부되었습니다
```
→ IAM 권한 확인
