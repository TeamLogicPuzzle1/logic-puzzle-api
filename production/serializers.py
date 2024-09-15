from rest_framework import serializers
from .models import Product
import datetime  # 추가된 import

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # 모든 필드를 직렬화

    def validate(self, data):
        # 유통기한이 현재 날짜보다 이전인지 확인
        if data.get('expiration_date') and data['expiration_date'] < datetime.date.today():
            raise serializers.ValidationError("The expiration date cannot be in the past.")

        # 추가적인 데이터 검증 로직을 여기서 처리
        return data