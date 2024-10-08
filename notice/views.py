from rest_framework import generics
from .models import Notice
from .serializers import NoticeSerializer

class NoticeListCreate(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer