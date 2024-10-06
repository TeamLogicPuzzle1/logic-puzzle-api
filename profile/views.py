from urllib import response

from drf_yasg.openapi import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.views import APIView

from profile.serializer import CreateProfileSerializer
from user.serializer import CreateUserSerializer


# Create your views here.
class MemberAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateProfileSerializer

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
            return response  # Response를 그대로 반환
        except Exception as e:
            # 여기서 처리되지 않은 예외를 포괄적으로 처리
            return Response({"message": f"알 수 없는 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)