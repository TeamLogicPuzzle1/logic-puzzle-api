from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializer import CreateUserSerializer, CheckPasswordSerializer


class SignupAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_id='register',
        operation_description='회원가입',
        tags=['User'],
        request_body=CreateUserSerializer,
        responses={200: 'success'}
    )
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            # Add user creation logic here
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


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
