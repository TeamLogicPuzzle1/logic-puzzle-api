import io
import os
import re
from datetime import datetime
from google.cloud import vision
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import logging
from datetime import date

# 환경 변수 설정 및 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 유통기한 형식을 확인하는 정규 표현식 (여러 형식 추가)
EXPIRATION_DATE_REGEX = (
    r'(\d{4}[\s.-]\d{1,2}[\s.-]\d{1,2})|'  # YYYY-MM-DD or YYYY.MM.DD or YYYY MM DD
    r'(\d{1,2}[\s/-]\d{1,2}[\s/-]\d{2,4})|'  # MM/DD/YYYY or MM-DD-YYYY or DD/MM/YYYY
    r'(\d{1,2}\s*[A-Za-z]{3,9}\s*\d{2,4})|'  # DD Month YYYY
    r'(\d{8})'  # YYYYMMDD
)

def get_vision_client():
    """
    최신 자격 증명을 사용하여 Vision API 클라이언트 생성
    """
    try:
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not credentials_path:
            raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS is not set in the .env file.")

        # OAuth 범위를 추가하여 자격 증명 설정
        scopes = ['https://www.googleapis.com/auth/cloud-platform']
        credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=scopes)

        # 토큰 갱신
        request = Request()
        if credentials.expired or not credentials.valid:
            credentials.refresh(request)

        client = vision.ImageAnnotatorClient(credentials=credentials)
        return client
    except Exception as e:
        logger.exception(f"Failed to create Vision API client: {str(e)}")
        raise

def extract_and_parse_expiration_date(image):
    """
    이미지 파일에서 유통기한을 추출하고 파싱하는 함수.
    인식 실패 시 오늘 날짜를 반환합니다.
    """
    try:
        # 최신 자격 증명을 사용해 Vision API 클라이언트 생성
        client = get_vision_client()

        # 이미지 파일의 포인터를 처음으로 이동
        image.seek(0)
        content = image.read()
        if not content:
            logger.error("Image content is empty.")
            return date.today()  # 오늘 날짜 반환

        image_obj = vision.Image(content=content)
        response = client.text_detection(image=image_obj)

        # 오류 발생 시 처리
        if response.error.message:
            logger.error(f"Error in API request: {response.error.message}")
            return date.today()  # 오늘 날짜 반환

        logger.info(f"API Response: {response}")
        texts = response.text_annotations

        # API 응답에서 텍스트 감지 결과 처리
        if texts:
            extracted_text = texts[0].description
            logger.info(f"Extracted Text: {extracted_text}")

            # 텍스트 후처리: 마침표(.)나 다른 불필요한 기호를 공백으로 대체
            cleaned_text = re.sub(r'[^0-9\s]', ' ', extracted_text)  # 숫자와 공백만 남기기
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # 여러 공백을 하나의 공백으로 변환
            logger.info(f"Cleaned Text: {cleaned_text}")

            # 유통기한 추출
            matches = re.findall(EXPIRATION_DATE_REGEX, cleaned_text)
            logger.info(f"Found matches: {matches}")

            if matches:
                for match_tuple in matches:
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
                            # 형식을 파싱 가능한 표준 형식으로 변경
                            formatted_match = match.replace('.', '-').replace(' ', '-')
                            parsed_date = datetime.strptime(formatted_match, '%Y-%m-%d').date()
                            logger.info(f"Parsed date (YYYY-MM-DD, YYYY.MM.DD, YYYY MM DD): {parsed_date}")
                            return parsed_date

                        # MM/DD/YYYY or MM-DD-YYYY 형식 처리
                        if '/' in match or '-' in match:
                            parsed_date = datetime.strptime(match,
                                                            '%m/%d/%Y').date() if '/' in match else datetime.strptime(
                                match, '%m-%d-%Y').date()
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
            return date.today()  # 유효한 날짜가 없을 경우 오늘 날짜 반환

    except Exception as e:
        logger.exception(f"An error occurred while processing the image: {str(e)}")
        return date.today()  # 예외 발생 시 오늘 날짜 반환


