from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Product
from user.models import User

class ProductCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(write_only=True)  # 입력에서만 user_id를 받음
    product_id = serializers.UUIDField(read_only=True)  # 응답에 product_id 포함

    class Meta:
        model = Product
        fields = ['product_id', 'name', 'expiration_date', 'category', 'location', 'quantity', 'memo', 'user_id']
        extra_kwargs = {
            'expiration_date': {'required': True},  # expiration_date 필수화
            'category': {'default': 1},  # 기본값 설정
            'location': {'default': 1},  # 기본값 설정
            'quantity': {'default': 1},  # 기본값 설정
        }

    def create(self, validated_data):
        # user_id로 User 객체 가져오기
        user_id = validated_data.pop('user_id')
        user = get_object_or_404(User, user_id=user_id)

        # Product 생성
        product = Product.objects.create(user=user, **validated_data)
        return product

    def update(self, instance, validated_data):
        # user_id를 업데이트하려는 경우 처리
        user_id = validated_data.pop('user_id', None)
        if user_id:
            user = get_object_or_404(User, user_id=user_id)
            validated_data['user'] = user

        # 기본 업데이트 로직 수행
        return super().update(instance, validated_data)

# ExpirationDateExtractSerializer를 클래스 외부로 이동
class ExpirationDateExtractSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)  # 이미지 파일 필수
