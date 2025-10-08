#!/usr/bin/env python3
"""
Git push 시 AWS Secrets Manager에서 시크릿을 로드하여 .deploy/production/.env 파일 생성
"""

import os
import sys
import json
from pathlib import Path


def load_secrets_from_aws():
    """AWS Secrets Manager에서 시크릿 로드"""
    try:
        # Secrets Manager 모듈 import
        sys.path.append("server/app/src")
        from core.secrets import SecretsManager

        # Secrets Manager 초기화
        secrets_manager = SecretsManager()

        # zsh 환경변수에서 시크릿 이름 가져오기
        secret_name = os.getenv("SECRET_NAME")
        if not secret_name:
            print("❌ SECRET_NAME 환경변수가 설정되지 않았습니다.")
            return None

        print(f"🔐 AWS Secrets Manager에서 시크릿 로드: {secret_name}")

        # 시크릿 가져오기
        secrets = secrets_manager.get_secret(secret_name)

        if secrets:
            print(f"✅ {len(secrets)}개의 시크릿 로드 성공")
            return secrets
        else:
            print("❌ 시크릿이 비어있습니다.")
            return None

    except Exception as e:
        print(f"❌ AWS Secrets Manager에서 시크릿 로드 실패: {e}")
        return None


def create_env_file(secrets, output_path):
    """시크릿을 .env 파일로 저장"""
    try:
        # 디렉토리 생성
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(
                "# =============================================================================\n"
            )
            f.write("# 자동 생성된 환경변수 파일 (AWS Secrets Manager에서 로드)\n")
            f.write(
                "# =============================================================================\n\n"
            )

            # SECRET_NAME 추가
            f.write(f"SECRET_NAME={os.getenv('SECRET_NAME', 'prod/intellius')}\n")

            # AWS 자격증명 추가 (zsh 환경변수에서)
            aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
            aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

            if aws_access_key:
                f.write(f"AWS_ACCESS_KEY_ID={aws_access_key}\n")
            if aws_secret_key:
                f.write(f"AWS_SECRET_ACCESS_KEY={aws_secret_key}\n")

            f.write(
                "\n# =============================================================================\n"
            )
            f.write("# AWS Secrets Manager에서 로드된 시크릿\n")
            f.write(
                "# =============================================================================\n"
            )

            # 시크릿 내용 추가
            for key, value in secrets.items():
                f.write(f"{key}={value}\n")

        print(f"✅ 환경변수 파일 생성 완료: {output_path}")
        return True

    except Exception as e:
        print(f"❌ 환경변수 파일 생성 실패: {e}")
        return False


def main():
    """메인 함수"""
    print("🔧 AWS Secrets Manager 환경변수 파일 생성")
    print("=" * 50)

    # zsh 환경변수 확인
    secret_name = os.getenv("SECRET_NAME")
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    print("🔍 zsh 환경변수 확인:")
    print(f"  SECRET_NAME: {'✅ 설정됨' if secret_name else '❌ 설정되지 않음'}")
    print(
        f"  AWS_ACCESS_KEY_ID: {'✅ 설정됨' if aws_access_key else '❌ 설정되지 않음'}"
    )
    print(
        f"  AWS_SECRET_ACCESS_KEY: {'✅ 설정됨' if aws_secret_key else '❌ 설정되지 않음'}"
    )

    if not secret_name:
        print("❌ SECRET_NAME 환경변수가 설정되지 않았습니다.")
        print("💡 다음 명령어로 환경변수를 설정하세요:")
        print("   export SECRET_NAME=prod/intellius")
        sys.exit(1)

    # AWS Secrets Manager에서 시크릿 로드
    print("\n🔐 AWS Secrets Manager에서 시크릿 로드 중...")
    secrets = load_secrets_from_aws()

    if not secrets:
        print("❌ 시크릿 로드에 실패했습니다.")
        sys.exit(1)

    # .env 파일 생성
    output_path = ".deploy/production/.env"
    print(f"\n📝 환경변수 파일 생성 중: {output_path}")

    if create_env_file(secrets, output_path):
        print("\n🎉 환경변수 파일 생성이 완료되었습니다!")
        print(f"📁 파일 위치: {output_path}")
        print("💡 이 파일은 git에 추적되지 않습니다.")
    else:
        print("\n❌ 환경변수 파일 생성에 실패했습니다.")
        sys.exit(1)


if __name__ == "__main__":
    main()
