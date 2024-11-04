from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializer import CreateUserSerializer
from user.service import UserService


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
        try:
            userData = request.data
            # serializer_class를 UserService로 전달
            response = UserService.userSave(userData, CreateUserSerializer)
            return response  # Response를 그대로 반환
        except Exception as e:
            # 여기서 처리되지 않은 예외를 포괄적으로 처리
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
                type=openapi.TYPE_STRING,
                description='id check',
                required=True,
            ),
        ],
        responses={200: '아이디 사용 가능', 400: '아이디 중복', 500: '서버 오류'}
    )
    def get(self, request):
        try:
            check_id = request.query_params.get('id')
            response = UserService.checkUserId(check_id)
            return response
        except Exception as e:
            # 여기서 처리되지 않은 예외를 포괄적으로 처리
            return Response({"message": f"알 수 없는 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SendVerificationCode(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(
        operation_id='verificationCode',
        operation_description='이메일 인증',
        tags=['User'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='사용자의 이메일 주소'),
            },
            required=['email']  # 필수 항목 지정
        ),
        responses={201: '회원가입 성공', 400: '잘못된 요청', 500: '서버 오류'}
    )
    def post(self, request):
        try:
            userEmail = request.query_params.get('email')
            response = UserService.sendVerifyCode(userEmail)
            return response  # Response를 그대로 반환
        except Exception as e:
            # 여기서 처리되지 않은 예외를 포괄적으로 처리
            return Response({"message": f"알 수 없는 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)