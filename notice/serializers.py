from rest_framework import serializers
from .models import Notice

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'created_at']
        extra_kwargs = {
            'title': {'required': True, 'help_text': '공지사항 제목입니다.'},
            'content': {'required': True, 'help_text': '공지사항 내용입니다.'},
        }