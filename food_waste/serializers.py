from rest_framework import serializers
from .models import FoodWaste
from user.models import User

class FoodWasteSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(write_only=True)  # 요청으로부터 user_id를 받기 위함

    class Meta:
        model = FoodWaste
        fields = ['user_id', 'quantity', 'date_recorded']  # date 필드를 포함시킴
        read_only_fields = ['date_recorded']

    def create(self, validated_data):
        # user_id를 이용해 User 객체를 가져오고 FoodWaste 객체 생성 시 user로 설정
        user_id = validated_data.pop('user_id')  # user_id를 validated_data에서 꺼내고 나머지 데이터만 사용
        user = User.objects.get(user_id=user_id)
        validated_data['user'] = user  # 나머지 데이터에 user를 추가
        return FoodWaste.objects.create(**validated_data)  # 이제 validated_data에 user가 포함되어 중복되지 않음