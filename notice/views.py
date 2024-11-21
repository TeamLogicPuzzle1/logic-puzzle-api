from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Notice
from .serializers import NoticeSerializer

class NoticeListCreate(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    @swagger_auto_schema(
        request_body=NoticeSerializer,
        responses={201: NoticeSerializer},
        operation_description="Create a notice."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    @swagger_auto_schema(
        responses={200: NoticeSerializer},
        operation_description="Retrieve a notice by ID."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)