import boto3
import json
import logging
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError, NoCredentialsError

logger = logging.getLogger(__name__)


class SecretsManager:
    """AWS Secrets Manager를 사용하여 시크릿을 관리하는 클래스"""

    def __init__(self, region_name: str = "ap-northeast-2"):
        """
        SecretsManager 초기화

        Args:
            region_name: AWS 리전 이름 (기본값: ap-northeast-2)
        """
        self.region_name = region_name
        self._client = None

    @property
    def client(self):
        """boto3 클라이언트 인스턴스 반환"""
        if self._client is None:
            try:
                self._client = boto3.client(
                    service_name="secretsmanager", region_name=self.region_name
                )
            except NoCredentialsError:
                logger.error(
                    "AWS 자격 증명을 찾을 수 없습니다. AWS CLI 설정을 확인하세요."
                )
                raise
        return self._client

    def get_secret(self, secret_name: str) -> Dict[str, Any]:
        """
        AWS Secrets Manager에서 시크릿 값을 가져옵니다.
        Args: secret_name: 시크릿 이름
        Returns:Dict[str, Any]: 시크릿 값 (JSON 파싱된 딕셔너리)
        """
        try:
            logger.info(f"시크릿 '{secret_name}' 가져오는 중...")

            response = self.client.get_secret_value(SecretId=secret_name)
            secret_string = response["SecretString"]

            # JSON 파싱
            try:
                secret_dict = json.loads(secret_string)
                logger.info(f"시크릿 '{secret_name}' 성공적으로 가져옴")
                return secret_dict
            except json.JSONDecodeError as e:
                logger.error(f"시크릿 '{secret_name}' JSON 파싱 실패: {e}")
                raise ValueError(f"시크릿 값이 유효한 JSON 형식이 아닙니다: {e}")

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ResourceNotFoundException":
                logger.error(f"시크릿 '{secret_name}'을 찾을 수 없습니다.")
                raise
            elif error_code == "InvalidRequestException":
                logger.error(f"시크릿 '{secret_name}' 요청이 잘못되었습니다.")
                raise
            elif error_code == "InvalidParameterException":
                logger.error(f"시크릿 '{secret_name}' 매개변수가 잘못되었습니다.")
                raise
            elif error_code == "DecryptionFailureException":
                logger.error(f"시크릿 '{secret_name}' 복호화에 실패했습니다.")
                raise
            elif error_code == "InternalServiceErrorException":
                logger.error(f"AWS Secrets Manager 내부 서비스 오류가 발생했습니다.")
                raise
            else:
                logger.error(f"시크릿 '{secret_name}' 가져오기 실패: {e}")
                raise

    def get_secret_value(self, secret_name: str, key: str) -> str:
        """
        시크릿에서 특정 키의 값을 가져옵니다.
        Args:
            secret_name: 시크릿 이름
            key: 가져올 키 이름
        Returns: str: 키에 해당하는 값
        """
        secret_dict = self.get_secret(secret_name)

        if key not in secret_dict:
            logger.error(f"시크릿 '{secret_name}'에서 키 '{key}'를 찾을 수 없습니다.")
            raise KeyError(f"키 '{key}'가 시크릿에 존재하지 않습니다.")

        return secret_dict[key]

    def list_secrets(self) -> list:
        """
        사용 가능한 시크릿 목록을 가져옵니다.
        Returns: list: 시크릿 이름 목록
        """
        try:
            response = self.client.list_secrets()
            logger.info(f"시크릿 목록 가져오기 성공: {response}")
            secret_names = [secret["Name"] for secret in response.get("SecretList", [])]
            logger.info(f"총 {len(secret_names)}개의 시크릿을 찾았습니다.")
            return secret_names
        except ClientError as e:
            logger.error(f"시크릿 목록 가져오기 실패: {e}")
            raise


# 전역 인스턴스
secrets_manager = SecretsManager()