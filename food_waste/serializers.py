from rest_framework import serializers
from .models import FoodWaste
from user.models import User


class FoodWasteSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(write_only=True)  # 요청에서 user_id를 받기 위해 사용
    quantity = serializers.ChoiceField(choices=FoodWaste.QUANTITY_CHOICES)  # choices 검증 추가
    action_type = serializers.ChoiceField(choices=FoodWaste.ACTION_TYPE_CHOICES)  # 0: 추가, 1: 감소

    class Meta:
        model = FoodWaste
        fields = ['user_id', 'quantity', 'action_type', 'date_recorded']
        read_only_fields = ['date_recorded']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')  # user_id 추출
        user = User.objects.get(user_id=user_id)
        validated_data['user'] = user
        return FoodWaste.objects.create(**validated_data)