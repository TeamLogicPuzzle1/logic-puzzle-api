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
        product = Product.objects.create(user=user, **validated_data)
        return product