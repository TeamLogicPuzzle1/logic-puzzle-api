# Create your views here.
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

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

        try:
            # RecipeService에서 음식과 재료 정보를 함께 조회
            response_data = RecipeService.recipeList(prod_names_list)

            if not response_data:
                return Response({'message': '레시피 데이터 없음'}, status=204)

            return Response({'recipes': response_data}, status=200)


        except DatabaseError:

            logger.error("레시피 데이터를 가져오는 중 오류 발생")

            return Response({'message': '레시피 데이터를 찾을 수 없습니다.'}, status=500)


        except Exception as e:

            logger.error(f"레시피 조회 중 서버 오류 발생: {e}")

            return Response({'message': '서버 오류가 발생했습니다.'}, status=500)

