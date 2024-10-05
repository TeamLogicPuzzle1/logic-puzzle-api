import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수 확인
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
print("Google Application Credentials Path:", credentials_path)

# 파일 존재 여부 확인
if credentials_path and os.path.isfile(credentials_path):
    print("Service account file exists.")
else:
    print("Service account file does not exist or path is incorrect.")