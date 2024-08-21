from rest_framework import serializers
from .models import FoodWaste

class FoodWasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodWaste
        fields = ['id', 'amount', 'date']