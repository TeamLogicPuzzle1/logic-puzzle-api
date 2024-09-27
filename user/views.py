from django.db import IntegrityError, DatabaseError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, logger
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User

from user.serializer import CreateUserSerializer, CheckPasswordSerializer


class SignupAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateUserSerializer

    @swagger_auto_schema(
        operation_id='register',
        operation_description='회원가입',
        tags=['User'],
        request_body=CreateUserSerializer,
        responses={201: '회원가입 성공', 400: '잘못된 요청', 500: '서버 오류'}
    )
    def post(self, request):
        user = request.data
        try:
            logger.debug("======>1")
            serializer = self.serializer_class(data=user)
            logger.debug("======>2")
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            logger.debug("======>3")
            return Response({"message": "회원가입이 성공적으로 완료되었습니다.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # 유효성 검사 실패 시 예외 처리
            return Response({"message": "입력 데이터가 유효하지 않습니다.", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            # 데이터베이스 중복 오류 처리 (예: 이미 존재하는 사용자)
            return Response({"message": "이미 존재하는 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            # 기타 데이터베이스 관련 예외 처리
            return Response({"message": "데이터베이스 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # 기타 예상치 못한 예외 처리
            return Response({"message": f"알 수 없는 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserCheckAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_id='checkIdDuplication',
        operation_description='아이디 중복 체크',
        tags=['User'],
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='id check',
                required=True,
            ),
        ],
        responses={200: 'success'}
    )
    def get(self, request):
        check_id = request.query_params.get('id')
        # Add logic to check if the ID is duplicated
        return Response(True, status=200)

    @swagger_auto_schema(
        operation_id='checkPassword',
        operation_description='비밀번호 체크',
        tags=['User'],
        request_body=CheckPasswordSerializer,
        responses={200: 'success'}
    )
    def post(self, request):
        serializer = CheckPasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Add password checking logic here
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)