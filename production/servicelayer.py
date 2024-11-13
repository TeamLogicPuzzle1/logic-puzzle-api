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

# 유통기한 형식을 확인하는 정규 표현식 (여러 형식 추가)
EXPIRATION_DATE_REGEX = (
    r'(\d{4}[\s.-]\d{1,2}[\s.-]\d{1,2})|'  # YYYY-MM-DD or YYYY.MM.DD or YYYY MM DD
    r'(\d{1,2}[\s/-]\d{1,2}[\s/-]\d{2,4})|'  # MM/DD/YYYY or MM-DD-YYYY or DD/MM/YYYY
    r'(\d{1,2}\s*[A-Za-z]{3,9}\s*\d{2,4})|'  # DD Month YYYY
    r'(\d{8})'  # YYYYMMDD
)

def parse_expiration_date(text):
    """Extracts the expiration date from the text using regex."""
    matches = re.findall(EXPIRATION_DATE_REGEX, text)
    logger.info(f"Found matches: {matches}")

    if matches:
        for match_tuple in matches:
            # match_tuple contains multiple groups due to multiple regex options, pick the non-empty one
            match = next((m for m in match_tuple if m), None)
            if not match:
                continue

            try:
                logger.info(f"Trying to parse date from match: {match}")

                # YYYYMMDD 형식 처리
                if len(match) == 8 and match.isdigit():
                    parsed_date = datetime.strptime(match, '%Y%m%d').date()
                    logger.info(f"Parsed date (YYYYMMDD): {parsed_date}")
                    return parsed_date

                # YYYY-MM-DD, YYYY.MM.DD, YYYY MM DD 처리
                if re.match(r'\d{4}[\s.-]\d{1,2}[\s.-]\d{1,2}', match):
                    parsed_date = datetime.strptime(match.replace('.', '-').replace(' ', '-'), '%Y-%m-%d').date()
                    logger.info(f"Parsed date (YYYY-MM-DD, YYYY.MM.DD, YYYY MM DD): {parsed_date}")
                    return parsed_date

                # MM/DD/YYYY or MM-DD-YYYY 형식 처리
                if '/' in match or '-' in match:
                    parsed_date = datetime.strptime(match, '%m/%d/%Y').date() if '/' in match else datetime.strptime(match, '%m-%d-%Y').date()
                    logger.info(f"Parsed date (MM/DD/YYYY or MM-DD-YYYY): {parsed_date}")
                    return parsed_date

                # DD Month YYYY 형식 처리
                if any(char.isalpha() for char in match):
                    parsed_date = datetime.strptime(match, '%d %B %Y').date()
                    logger.info(f"Parsed date (DD Month YYYY): {parsed_date}")
                    return parsed_date

            except ValueError as e:
                logger.warning(f"Failed to parse date '{match}' with error: {e}")
                continue

    logger.warning("No valid expiration date found after parsing.")
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

            # 텍스트 후처리: 마침표(.)나 다른 불필요한 기호를 공백으로 대체
            cleaned_text = re.sub(r'[.\-]', ' ', extracted_text)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # 여분의 공백 제거
            logger.info(f"Cleaned Text: {cleaned_text}")  # 수정된 텍스트 로그로 출력

            # 유통기한 추출
            expiration_date = parse_expiration_date(cleaned_text)
            if expiration_date:
                return expiration_date
            else:
                logger.warning("No valid expiration date found in the text.")
                return None

    except Exception as e:
        logger.exception(f"An error occurred while processing the image: {str(e)}")
        return None  # 예외 발생 시 None 반환