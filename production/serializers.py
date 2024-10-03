from rest_framework import serializers
from .models import Product

class ProductCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)  # Add this field to handle image files

    class Meta:
        model = Product
        fields = '__all__'