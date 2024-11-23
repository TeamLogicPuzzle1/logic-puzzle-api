import logging
import os
import re
from datetime import datetime

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.cloud import vision
from google.oauth2 import service_account
from rest_framework import status
from rest_framework.response import Response

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
        # 환경 변수에서 자격 증명 경로 가져오기
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not credentials_path:
            raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS is not set in the environment.")
    except Exception as e:
        logger.exception(f"Failed to retrieve credentials path: {str(e)}")
        raise EnvironmentError("자격 증명 경로를 가져오는 데 실패했습니다. 환경 변수를 확인하세요.") from e

    try:
        # OAuth 범위를 추가하여 자격 증명 설정
        scopes = ['https://www.googleapis.com/auth/cloud-platform']
        credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=scopes)
    except FileNotFoundError as fnfe:
        logger.exception(f"Credentials file not found: {str(fnfe)}")
        raise FileNotFoundError("자격 증명 파일을 찾을 수 없습니다. 경로를 확인하세요.") from fnfe
    except Exception as e:
        logger.exception(f"Failed to load credentials: {str(e)}")
        raise ValueError("자격 증명을 로드하는 데 실패했습니다.") from e

    try:
        # 자격 증명 유효성 확인 및 갱신
        request = Request()
        if credentials.expired or not credentials.valid:
            credentials.refresh(request)
            logger.info("Credentials successfully refreshed.")
    except Exception as e:
        logger.exception(f"Failed to refresh credentials: {str(e)}")
        raise RuntimeError("자격 증명 갱신에 실패했습니다.") from e

    try:
        # Vision API 클라이언트 생성
        client = vision.ImageAnnotatorClient(credentials=credentials)
        logger.info("Vision API client successfully created.")
        return client
    except Exception as e:
        logger.exception(f"Failed to create Vision API client: {str(e)}")
        raise RuntimeError("Vision API 클라이언트를 생성하는 데 실패했습니다.") from e


def extract_and_parse_expiration_date(image):
    """
    이미지 파일에서 유통기한을 추출하고 파싱하는 함수.
    """
    try:
        # 최신 자격 증명을 사용해 Vision API 클라이언트 생성
        client = get_vision_client()
    except Exception as e:
        logger.exception(f"Failed to initialize Vision API client: {e}")
        return Response({"message": "Vision API 초기화 오류."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        # 이미지 파일의 포인터를 처음으로 이동
        image.seek(0)
        content = image.read()
        if not content:
            logger.error("Image content is empty.")
            return Response({"message": "이미지가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception(f"Failed to process image content: {e}")
        return Response({"message": "이미지 처리 오류."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    image_obj = vision.Image(content=content)
    response = client.text_detection(image=image_obj)

    try:
        # Vision API를 사용해 텍스트 감지
        image_obj = vision.Image(content=content)
        response = client.text_detection(image=image_obj)

        # Vision API 오류 처리
        if response.error.message:
            logger.error(f"Error in API request: {response.error.message}")
            return Response({"message": "Vision API 오류 발생."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.exception(f"Error during Vision API request: {e}")
        return Response({"message": "Vision API 요청 처리 오류."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    try:
        logger.info(f"API Response: {response}")
        texts = response.text_annotations
        if not texts:
            return Response({"message": "텍스트를 감지하지 못했습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 텍스트 후처리
        extracted_text = texts[0].description
        logger.info(f"Extracted Text: {extracted_text}")
        cleaned_text = re.sub(r'[^0-9\s]', ' ', extracted_text)  # 숫자와 공백만 남기기
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # 여러 공백을 하나의 공백으로 변환
        logger.info(f"Cleaned Text: {cleaned_text}")
    except Exception as e:
        logger.exception(f"Error processing text annotations: {e}")
        return Response({"message": "텍스트 처리 오류."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
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
                        return Response({"expiration_date": str(parsed_date.strftime('%Y.%m.%d'))}, status=status.HTTP_200_OK)

                    # YYYY-MM-DD, YYYY.MM.DD, YYYY MM DD 처리
                    if re.match(r'\d{4}[\s.-]\d{1,2}[\s.-]\d{1,2}', match):
                        # 형식을 파싱 가능한 표준 형식으로 변경
                        formatted_match = match.replace('.', '-').replace(' ', '-')
                        parsed_date = datetime.strptime(formatted_match, '%Y-%m-%d').date()
                        logger.info(f"Parsed date (YYYY-MM-DD, YYYY.MM.DD, YYYY MM DD): {parsed_date}")
                        return Response({"expiration_date": str(parsed_date.strftime('%Y.%m.%d'))}, status=status.HTTP_200_OK)


                    # MM/DD/YYYY or MM-DD-YYYY 형식 처리
                    if '/' in match or '-' in match:
                        parsed_date = datetime.strptime(match,
                                                        '%m/%d/%Y').date() if '/' in match else datetime.strptime(
                            match, '%m-%d-%Y').date()
                        logger.info(f"Parsed date (MM/DD/YYYY or MM-DD-YYYY): {parsed_date}")
                        return Response({"expiration_date": str(parsed_date.strftime('%Y.%m.%d'))}, status=status.HTTP_200_OK)

                    # DD Month YYYY 형식 처리
                    if any(char.isalpha() for char in match):
                        parsed_date = datetime.strptime(match, '%d %B %Y').date()
                        logger.info(f"Parsed date (DD Month YYYY): {parsed_date}")
                        return Response({"expiration_date": str(parsed_date.strftime('%Y.%m.%d'))}, status=status.HTTP_200_OK)

                except ValueError as ve:
                    logger.warning(f"Failed to parse date '{match}' with error: {ve}")
                    continue

        logger.warning("No valid expiration date found after parsing.")
        return Response({"message": "유통기한 유효성 체크 오류."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        logger.exception(f"Error extracting expiration date: {e}")
        return Response({"message": "유통기한 추출 오류."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

