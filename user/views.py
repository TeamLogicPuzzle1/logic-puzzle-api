import logging


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializer import CreateUserSerializer, LoginSerializer, CheckIdSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import check_password, make_password
from user.service import UserService, LoginService, ChpassService
logger = logging.getLogger(__name__)

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


class SendVerifyCode(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_id='sendVerifyCode',
        operation_description='이메일 인증',
        tags=['User'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL,
                                        description='사용자의 이메일 주소'),
            },
            required=['email']  # 필수 항목 지정
        ),
        responses={201: '이메일 전송 성공', 400: '잘못된 요청', 500: '서버 오류'}
    )
    def post(self, request):
        try:
            userEmail = request.data.get('email')
            response = UserService.sendVerifyCode(userEmail)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            # 여기서 처리되지 않은 예외를 포괄적으로 처리
            return Response({"message": f"알 수 없는 오류가 발생했습니다: {str(e)}", "data": False},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckVerifyCode(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_id='checkVerifyCode',
        operation_description='인증번호 체크',
        tags=['User'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'code': openapi.Schema(type=openapi.TYPE_INTEGER, format=openapi.TYPE_INTEGER,
                                       description='인증번호'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL,
                                        description='이메일 주소'),
            },
            required=['code', 'email'],  # 필수 항목 지정
        ),
        responses={200: '인증 성공', 400: '잘못된 요청', 500: '서버 오류'}
    )
    def post(self, request):
        try:
            code = request.data.get('code')
            email = request.data.get('email')
            response = UserService.checkVerifyCode(code, email)
            return response
        except Exception as e:
            # 여기서 처리되지 않은 예외를 포괄적으로 처리
            return Response({"message": f"알 수 없는 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPIView(APIView):
    permission_classes = []  # 모든 사용자에게 접근 허용

    @swagger_auto_schema(
        operation_id="user_login",
        operation_description="사용자 로그인을 수행합니다.",
        tags=["User"],
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="로그인 성공",
                examples={
                    "application/json": {
                        "message": "Login successful",
                        "user_id": "testuser"
                    }
                }
            ),
            401: openapi.Response(
                description="잘못된 비밀번호",
                examples={
                    "application/json": {
                        "message": "Invalid password"
                    }
                }
            ),
            404: openapi.Response(
                description="존재하지 않는 사용자",
                examples={
                    "application/json": {
                        "message": "User ID not found"
                    }
                }
            )
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["user_id"]

        return Response(
            {"message": "Login successful", "user_id": user_id},
            status=status.HTTP_200_OK
        )

class FindUserIdWithVerificationAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_id='findUserIdWithVerification',
        operation_description='이메일 인증 후 아이디 찾기',
        tags=['User'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description='사용자의 이메일 주소'
                ),
                'is_verified': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description='이메일 인증 여부 (True or False)'
                )
            },
            required=['email', 'is_verified']
        ),
        responses={
            200: openapi.Response(
                description="아이디 찾기 성공",
                examples={
                    "application/json": {
                        "message": "아이디 찾기 성공",
                        "user_id": "john_doe"
                    }
                }
            ),
            400: openapi.Response(
                description="인증 실패 또는 잘못된 요청",
                examples={
                    "application/json": {
                        "message": "Invalid verification or email not verified",
                        "data": False
                    }
                }
            ),
            404: openapi.Response(
                description="사용자 없음",
                examples={
                    "application/json": {
                        "message": "User not found",
                        "data": False
                    }
                }
            )
        }
    )
    def post(self, request):
        try:
            # 파라미터 추출
            email = request.data.get('email')
            is_verified = request.data.get('is_verified')

            # 이메일 인증 여부 확인
            if not is_verified:
                return Response({"message": "이메일 인증에 실패했습니다.", "data": False}, status=status.HTTP_400_BAD_REQUEST)

            # 이메일로 사용자 찾기
            try:
                user = User.objects.get(email=email)
                return Response({
                    "message": "아이디 찾기 성공",
                    "user_id": user.user_id
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({
                    "message": "사용자를 찾을 수 없습니다.",
                    "data": False
                }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "message": f"알 수 없는 오류가 발생했습니다: {str(e)}",
                "data": False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CheckIdAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_id='findUserIdWithVerification',
        operation_description='이메일 인증 후 아이디 찾기',
        tags=['User'],
        request_body=CheckIdSerializer,  # 시리얼라이저를 사용하여 요청 데이터 검증
        responses={
            200: openapi.Response(
                description="아이디 찾기 성공",
                examples={
                    "application/json": {
                        "message": "아이디 찾기 성공",
                        "user_id": "john_doe"
                    }
                }
            ),
            400: openapi.Response(
                description="인증 실패 또는 잘못된 요청",
                examples={
                    "application/json": {
                        "message": "Invalid verification or email not verified",
                        "data": False
                    }
                }
            ),
            404: openapi.Response(
                description="사용자 없음",
                examples={
                    "application/json": {
                        "message": "User not found",
                        "data": False
                    }
                }
            )
        }
    )
    def post(self, request):
        # 시리얼라이저로 입력 데이터 검증
        serializer = CheckIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 유효성 검사를 수행합니다.

        # 시리얼라이저 검증 후 데이터 추출
        email = serializer.validated_data['email']
        is_verified = serializer.validated_data['is_verified']

        if not is_verified:
            logger.warning("이메일 인증 실패")
            return Response({"message": "이메일 인증에 실패했습니다.", "data": False}, status=status.HTTP_400_BAD_REQUEST)

        # 이메일로 사용자 찾기
        try:
            user = User.objects.get(email=email)
            return Response({
                "message": "아이디 찾기 성공",
                "user_id": user.user_id
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.error("User not found with the given email.")
            return Response({
                "message": "사용자를 찾을 수 없습니다.",
                "data": False
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {str(e)}")
            return Response({
                "message": f"알 수 없는 오류가 발생했습니다: {str(e)}",
                "data": False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ChpasswdAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    """
    비밀번호 변경/재설정 API
    """

    @swagger_auto_schema(
        operation_id="reset_or_change_password",
        operation_description="비밀번호 재설정(비로그인 상태) 또는 변경(로그인 상태)을 수행합니다.",
        tags=["User"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="사용자 ID"
                ),
                "is_verified": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="이메일 인증 여부 (비로그인 상태에서 필요)"
                ),
                "current_password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="현재 비밀번호 (로그인 상태에서 필요)"
                ),
                "new_password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="새 비밀번호"
                ),
                "confirm_new_password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="새 비밀번호 확인"
                ),
            },
            required=["user_id", "new_password", "confirm_new_password"],
        ),
        responses={
            200: openapi.Response(
                description="비밀번호 변경 성공",
                examples={
                    "application/json": {
                        "message": "Password updated successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="잘못된 요청",
                examples={
                    "application/json": {
                        "message": "Invalid request data"
                    }
                }
            ),
            404: openapi.Response(
                description="사용자 없음",
                examples={
                    "application/json": {
                        "message": "User not found"
                    }
                }
            )
        }
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        is_verified = request.data.get("is_verified")  # 비로그인 상태 여부
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        confirm_new_password = request.data.get("confirm_new_password")

        # 새 비밀번호와 확인 비밀번호 검증
        if new_password != confirm_new_password:
            return Response(
                {"message": "Passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if is_verified is not None:  # 비로그인 상태에서 이메일 인증
            result = ChpassService.reset_password(user_id, is_verified, new_password)
        else:  # 로그인 상태에서 비밀번호 변경
            result = ChpassService.change_password(user_id, current_password, new_password)

        if not result["success"]:
            return Response({"message": result["error"]}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
