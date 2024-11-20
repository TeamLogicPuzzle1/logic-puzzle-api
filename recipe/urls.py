from django.urls import path

from recipe.views import RecipeListAPIView

app_name = 'recipe'

urlpatterns = [
    path('recipes', RecipeListAPIView.as_view(), name='recipes'),
]
