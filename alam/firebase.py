import os
from firebase_admin import credentials
import firebase_admin

# 현재 파일의 절대 경로를 기준으로 config 폴더의 alarmserviceAccountKey.json 파일 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(base_dir, '../config/alarmserviceAccountKey.json')  # 경로 수정

# 경로 확인 (디버그 용)
print("Credential file path:", cred_path)

# Firebase 앱 초기화
cred = credentials.Certificate(cred_path)
firebase_app = firebase_admin.initialize_app(cred)