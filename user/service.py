from django.core.mail import EmailMessage
from django.core.mail.backends.smtp.EmailBackend import ssl_context
from django.db import IntegrityError, DatabaseError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from user.models import User
from user.serializer import EmailThread
from util.emailHelper import sendEmailHelper


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

    @classmethod
    def sendVerifyCode(cls, email):
        try:
            # 인증 코드 생성 및 이메일 전송 로직
            code = sendEmailHelper.makeRandomCode()  # 인증 코드 생성 함수 호출
            message = code
            subject = "EMAIL 제목"
            to = [email]

            mail = EmailMessage(subject=subject, body=message, to=to)
            mail.content_subtype = "html"  # 이메일을 HTML 형식으로 설정
            mail.send(fail_silently=False, connection=None, ssl_context=ssl_context)

            return Response({"message": "Success to send Email", "data": True}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            # 예외 처리: 이메일 전송 실패 시 에러 메시지 반환
            return Response({"message": f"Failed to send Email: {str(e)}", "data": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
