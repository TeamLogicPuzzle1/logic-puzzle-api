# serviceslayer.py
import firebase_admin
from firebase_admin import credentials, messaging

# Firebase 초기화 함수 (앱 시작 시 한 번만 호출되도록 구성)
def initialize_firebase():
    if not firebase_admin._apps:  # Firebase가 이미 초기화되어 있는지 확인
        cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

# 푸쉬 알림 전송 함수
def send_push_notification(token, title, body):
    # 메시지 설정
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token,
    )

    # 메시지 전송
    response = messaging.send(message)
    print("Successfully sent message:", response)