import logging
from smtplib import SMTPException, SMTPConnectError, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError

import redis
from celery import shared_task
from django.core.mail import EmailMessage
from django.db import IntegrityError, DatabaseError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password, make_password
import bcrypt

from user.models import User
from util.emailHelper import sendEmailHelper

logger = logging.getLogger(__name__)

client = redis.StrictRedis(host='redis_service', port=6379, db=0)

class UserService:
    def userSave(data, serializer_class):
        try:
            # 전달받은 데이터를 이용해 serializer 객체 생성
            serializer = serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({"message": "회원가입이 성공적으로 완료되었습니다.", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # 유효성 검사 실패 시 예외 처리
            return Response({"message": "회원가입 양식에 맞지않습니다.", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            # 데이터베이스 중복 오류 처리 (예: 이미 존재하는 사용자)
            return Response({"message": "이미 존재하는 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            # 기타 데이터베이스 관련 예외 처리
            return Response({"message": "데이터베이스 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # 기타 예상치 못한 예외 처리
            return Response({"message": f"알 수 없는 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def checkUserId(cls, data):
        if User.objects.filter(user_id=data).exists():
            return Response({"message": "이미 사용 중인 아아디입니다.", "data": False},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "사용 가능한 아이디입니다.", "data": True},
                            status=status.HTTP_200_OK)

    @shared_task
    def sendVerifyCode(email):
        try:
            logger.info("client.ping() = " + str(client.ping()))
            logger.info("email =" + email)
            # 인증 코드 생성 및 이메일 전송 로직
            code = sendEmailHelper.makeRandomCode()  # 인증 코드 생성 함수 호출
            message = code
            client.set(email, code, ex=300)
            subject = "%s" % "[냉집사] 이메일 인증 코드 안내"
            to = [email]
            mail = EmailMessage(subject=subject, body=message, to=to)
            mail.content_subtype = "html"
            mail.send()
            logger.info("Email sent successfully")
            return {"message": "Success to send Email", "data": True}
        except SMTPRecipientsRefused as e:
            logger.error(f"Invalid recipient email address: {e}")
            return {"message": "Invalid recipient email address", "data": False}
        except SMTPSenderRefused as e:
            logger.error(f"Sender address refused: {e}")
            return {"message": "Sender address refused", "data": False}
        except SMTPDataError as e:
            logger.error(f"SMTP data error: {e}")
            return {"message": "SMTP data error", "data": False}
        except SMTPConnectError as e:
            logger.error(f"SMTP connection failed: {e}")
            return {"message": "SMTP connection failed", "data": False}
        except SMTPException as e:
            logger.error(f"Failed to send email: {e}")
            return {"message": f"Failed to send Email: {str(e)}", "data": False}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"message": "Unexpected error occurred", "data": False}
        except redis.ConnectionError:
            logger.error("Failed to connect to Redis.")
            return {"message": "Redis connection failed", "data": False}

    @classmethod
    def checkVerifyCode(cls, code, email):
        redisVal = client.get(email)

        if redisVal is None:
            # Log the error or handle it accordingly
            logger.error("No verification code found for the provided email.")
            return Response({"message": "인증 코드가 존재하지 않습니다.", "data": False}, status=status.HTTP_400_BAD_REQUEST)

        # Decode the value if it exists
        answer = redisVal.decode('utf-8')
        logger.info("answer = " + str(type(answer)) + ":::" + answer)
        logger.info("code = " + str(type(code)) + ":::" + str(code))

        if str(code) == answer:
            client.delete(email)
            return Response({"message": "메일 인증이 성공하였습니다.", "data": True}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "메일 인증이 실패하였습니다.", "data": False}, status=status.HTTP_400_BAD_REQUEST)

class LoginService:
    @staticmethod
    def userSave(data, serializer_class):
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User registered successfully."},
            status=status.HTTP_201_CREATED
        )


class ChpassService:
    @staticmethod
    def reset_password(user_id, is_verified, new_password):
        if not is_verified:
            return {"success": False, "error": "Email verification required."}

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return {"success": False, "error": "User not found."}

        hashed_password = bcrypt.hashpw(
            new_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        user.password = hashed_password
        user.save()
        return {"success": True}

    @staticmethod
    def change_password(user_id, current_password, new_password):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return {"success": False, "error": "User not found."}

        if not bcrypt.checkpw(current_password.encode('utf-8'), user.password.encode('utf-8')):
            return {"success": False, "error": "Invalid current password."}

        hashed_password = bcrypt.hashpw(
            new_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        user.password = hashed_password
        user.save()
        return {"success": True}
