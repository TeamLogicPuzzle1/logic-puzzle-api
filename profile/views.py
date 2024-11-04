from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from profile.serializer import CreateProfileSerializer, LoginSerializer
from profile.service import ProfileService


# Create your views here.
class MemberAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateProfileSerializer

    @swagger_auto_schema(
        operation_id='add member',
        operation_description='멤버 추가',
        tags=['Profile'],
        request_body=CreateProfileSerializer,
        responses={201: '멤버추가 성공', 400: '잘못된 요청', 500: '서버 오류'}
    )
    def post(self, request):
        try:
            userData = request.data
            response = ProfileService.profileSave(userData, CreateProfileSerializer)
            return response  # Response를 그대로 반환
        except Exception as e:
            # 여기서 처리되지 않은 예외를 포괄적으로 처리
            return Response({"message": f"알 수 없는 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_id='login',
        operation_description='로그인',
        tags=['Profile'],
        request_body=LoginSerializer,
        responses={201: '로그인 성공', 400: '잘못된 요청', 500: '서버 오류'}
    )
    def post(self, request):
        try:
            userData = request.data
            response = ProfileService.login(userData, LoginSerializer)
            return response  # Response를 그대로 반환
        except Exception as e:
            # 여기서 처리되지 않은 예외를 포괄적으로 처리
            return Response({"message": f"알 수 없는 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)