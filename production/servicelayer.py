import io
import os
import re
from datetime import datetime
from google.cloud import vision
from dotenv import load_dotenv

import os
from dotenv import load_dotenv



# .env 파일에서 환경 변수 로드
load_dotenv()

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


# 이미지에서 유통기한 추출
def extract_expiration_date_from_image(image_file):
    # 이미지 파일을 읽어 content로 변환
    content = image_file.read()

    # Google Vision API 클라이언트 생성
    client = vision.ImageAnnotatorClient()

    # 이미지 데이터로 Image 객체 생성
    image = vision.Image(content=content)

    # 텍스트 감지 요청
    response = client.text_detection(image=image)

    # API 응답에서 텍스트 감지 결과 처리
    if response.error.message:
        print("Error in API request:", response.error.message)
        return datetime.now().date()  # 오류 발생 시 현재 날짜 반환

    if response.text_annotations:
        extracted_text = response.text_annotations[0].description
        expiration_date = parse_expiration_date(extracted_text)
        # 반환된 유통기한이 None이면 현재 날짜 반환
        if expiration_date is None:
            expiration_date = datetime.now().date()
        return expiration_date

    return datetime.now().date()  # 이미지에서 텍스트가 감지되지 않았을 경우 현재 날짜 반환

# 유통기한 문자열을 날짜 형식으로 파싱
def parse_expiration_date(text):
    date_patterns = [
        r'\b\d{8}\b',  # 8자리 숫자 (예: YYYYMMDD, MMDDYYYY, DDMMYYYY)
        r'\b\d{6}\b',  # 6자리 숫자 (예: YYMMDD, DDMMYY)
    ]

    current_date = datetime.now()  # 현재 날짜

    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group(0)
            extracted_date = extract_date_with_validation(date_str)
            return extracted_date

    # 일치하는 날짜 형식이 없을 경우 현재 날짜 반환
    return current_date.date()

# 숫자 형식에 따른 날짜 변환 로직
def extract_date_with_validation(date_str):
    current_date = datetime.now()

    if len(date_str) == 8:
        year = int(date_str[0:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])

        if 1 <= month <= 12 and 1 <= day <= 31:
            try:
                extracted_date = datetime(year, month, day)
                if extracted_date >= current_date:
                    return extracted_date.date()
            except ValueError:
                pass

    elif len(date_str) == 6:
        year = int(date_str[0:2]) + 2000
        month = int(date_str[2:4])
        day = int(date_str[4:6])

        if 1 <= month <= 12 and 1 <= day <= 31:
            try:
                extracted_date = datetime(year, month, day)
                if extracted_date >= current_date:
                    return extracted_date.date()
            except ValueError:
                pass

    return current_date.date()