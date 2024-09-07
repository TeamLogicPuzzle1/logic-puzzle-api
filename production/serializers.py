from rest_framework import serializers
from .models import Product
<<<<<<< HEAD
=======
import datetime

>>>>>>> b1a42273d14747a7e473f1904d1d7b508364f847

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
<<<<<<< HEAD
        fields = '__all__'
=======
        fields = '__all__'

    def validate(self, data):
        # 예: 유통기한이 현재 날짜보다 이전인지 확인
        if data.get('expiration_date') and data['expiration_date'] < datetime.date.today():
            raise serializers.ValidationError("The expiration date cannot be in the past.")

        # 추가적인 데이터 검증 로직을 여기서 처리
        return data
>>>>>>> b1a42273d14747a7e473f1904d1d7b508364f847
