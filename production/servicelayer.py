import io
import os
import re
from datetime import datetime
from google.cloud import vision
from dotenv import load_dotenv
import logging
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# .env 파일에서 환경 변수 로드
load_dotenv()

credentials_path = env('GOOGLE_APPLICATION_CREDENTIALS')

if not credentials_path:
    raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS is not set in the .env file.")

# 유통기한 형식을 확인하는 정규 표현식
EXPIRATION_DATE_REGEX = r'(\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}-\d{1,2}-\d{2,4}|\d{1,2}\s*[A-Za-z]{3,9}\s*\d{2,4}|\d{8})'


def parse_expiration_date(text):
    """Extracts the expiration date from the text using regex."""
    matches = re.findall(EXPIRATION_DATE_REGEX, text)
    if matches:
        for match in matches:
            try:
                # YYYYMMDD 형식 처리
                if len(match) == 8 and match.isdigit():
                    return datetime.strptime(match, '%Y%m%d').date()

                # 시도해보는 다른 날짜 형식
                if '/' in match:
                    return datetime.strptime(match, '%m/%d/%Y').date()
                elif '-' in match:
                    return datetime.strptime(match, '%m-%d-%Y').date()
                else:
                    return datetime.strptime(match, '%d %B %Y').date()
            except ValueError:
                continue
    return None


# 이미지에서 유통기한 추출
def extract_expiration_date_from_image(image_file):
    try:
        # Google Vision API 클라이언트 생성
        client = vision.ImageAnnotatorClient()

        # 이미지 파일의 포인터를 처음으로 이동
        image_file.seek(0)

        # 이미지 파일을 읽어서 Vision API에 전달하기 위한 형식으로 변환
        content = image_file.read()  # 이미지 파일의 내용을 읽음
        if not content:
            logger.error("Image content is empty.")
            return None

        image = vision.Image(content=content)

        # Vision API에 요청
        response = client.text_detection(image=image)

        # API 응답을 로깅
        if response.error.message:
            logger.error(f"Error in API request: {response.error.message}")
            return None  # 오류 발생 시 None 반환

        logger.info(f"API Response: {response}")

        texts = response.text_annotations

        # API 응답에서 텍스트 감지 결과 처리
        if texts:
            extracted_text = texts[0].description
            logger.info(f"Extracted Text: {extracted_text}")  # 추출된 텍스트 로그로 출력
            expiration_date = parse_expiration_date(extracted_text)
            if expiration_date:
                return expiration_date
            else:
                logger.warning("No valid expiration date found in the text.")
                return None

    except Exception as e:
        logger.exception(f"An error occurred while processing the image: {str(e)}")
        return None  # 예외 발생 시 None 반환