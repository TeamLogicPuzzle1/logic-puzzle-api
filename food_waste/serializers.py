# serializers.py
from rest_framework import serializers
from .models import FoodWaste

class FoodWasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodWaste
        fields = ['quantity', 'date_recorded']  # amount 필드는 제거
        read_only_fields = ['date_recorded']  # 자동 설정 필드로 읽기 전용