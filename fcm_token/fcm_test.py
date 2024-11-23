import sys
import os
import logging

# 현재 파일이 있는 폴더를 Python 모듈 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# servicelayer 모듈 가져오기
from servicelayer import send_push_notification

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    test_token = "your_fcm_test_token_here"  # 테스트용 FCM 토큰
    title = "테스트 알림"
    body = "이것은 테스트 푸시 알림입니다."

    try:
        send_push_notification(test_token, title, body)
    except Exception as e:
        logger.error(f"알림 전송 중 오류 발생: {str(e)}")
    else:
        logger.info("알림이 성공적으로 전송되었습니다.")