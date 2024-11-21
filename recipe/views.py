# Create your views here.
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.views import APIView

from recipe.service import RecipeService

logger = logging.getLogger(__name__)


class RecipeListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_id='get recipeList',
        operation_description='추천 레시 리스트 조회',
        tags=['Recipe'],
        manual_parameters=[
            openapi.Parameter(
                name='prodNames',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                description='production-names',
                required=True,
            ),
        ],
        responses={201: '레시피 조회 성공', 204: '레시피 데이터 없음', 400: '잘못된 요청', 500: '서버 오류'}
    )
    def get(self, request):
        prod_names = request.query_params.get('prodNames', "")
        prod_names_list = prod_names.split(',')
        response = RecipeService.recipeList(prod_names_list)
        return response
