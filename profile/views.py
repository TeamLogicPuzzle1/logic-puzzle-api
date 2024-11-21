from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from profile.serializer import CreateProfileSerializer
from profile.service import ProfileService


# Create your views here.
class MemberAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_id='add_member',
        operation_description='멤버 추가',
        tags=['Profile'],
        request_body=CreateProfileSerializer,
        responses={201: '멤버 추가 성공', 400: '잘못된 요청', 500: '서버 오류'}
    )
    def post(self, request):
        try:
            user_data = request.data
            response = ProfileService.profileSave(user_data, CreateProfileSerializer)
            return response  # Response를 그대로 반환
        except Exception as e:
            # 여기서 처리되지 않은 예외를 포괄적으로 처리
            return Response({"message": f"알 수 없는 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MemberListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_id='get memberList',
        operation_description='멤버 리스트 조회',
        tags=['Profile'],
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='user id',
                required=True,
            ),
        ],
        responses={201: '멤버조회 성공', 204: '멤버 없음', 400: '잘못된 요청', 500: '서버 오류'}
    )
    def get(self, request):
        try:
            user_id = request.query_params.get('id')
            response = ProfileService.getProfileList(user_id)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            # 여기서 처리되지 않은 예외를 포괄적으로 처리
            return Response({"message": f"알 수 없는 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
