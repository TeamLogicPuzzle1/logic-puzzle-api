import json
import requests
from google.oauth2 import service_account
import google.auth.transport.requests
from dotenv import load_dotenv
import os
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# .env 파일에서 환경 변수 불러오기
load_dotenv()

# 환경 변수에서 필요한 정보 가져오기
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')  # 서비스 계정 JSON 파일 경로
FCM_URL = 'https://fcm.googleapis.com/v1/projects/42293250807/messages:send'  # 실제 프로젝트 ID

# 서비스 계정 키 파일을 사용해 자격 증명 생성
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# 헤더 설정 (인증 토큰 포함)
def get_headers():
    # 액세스 토큰 가져오기
    auth_request = google.auth.transport.requests.Request()
    credentials.refresh(auth_request)
    return {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json; UTF-8",
    }

# 푸시 알림 전송 함수
def send_push_notification(token, title, body):
    logger.info("send_push_notification 함수가 호출되었습니다.")
    headers = get_headers()
    message = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }

    try:
        response = requests.post(FCM_URL, headers=headers, json=message)
        response.raise_for_status()
        logger.info("푸시 알림이 성공적으로 전송되었습니다.")
    except requests.exceptions.HTTPError as e:
        logger.error(f"푸시 알림 전송 중 오류 발생: {str(e)}")
        logger.error(f"응답 본문: {response.text}")
        raise