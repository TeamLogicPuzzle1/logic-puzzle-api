from rest_framework import generics
from .models import FoodWaste
from .serializers import FoodWasteSerializer

class FoodWasteListCreate(generics.ListCreateAPIView):
    queryset = FoodWaste.objects.all()
    serializer_class = FoodWasteSerializer

class FoodWasteDetail(generics.RetrieveUpdateAPIView):
    queryset = FoodWaste.objects.all()
    serializer_class = FoodWasteSerializer