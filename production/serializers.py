from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Product
from user.models import User

class ProductCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(write_only=True)
    product_id = serializers.UUIDField(read_only=True)  # 응답에 product_id 포함

    class Meta:
        model = Product
        fields = ['product_id', 'name', 'expiration_date', 'category', 'location', 'quantity', 'memo', 'image', 'user_id']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = get_object_or_404(User, user_id=user_id)

        # 기본값 처리
        validated_data.setdefault('category', 1)  # category 기본값
        validated_data.setdefault('location', 1)  # location 기본값
        validated_data.setdefault('quantity', 1)  # quantity 기본값

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