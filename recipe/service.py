import logging
import random
import re

from django.db import DatabaseError
from rest_framework import status
from rest_framework.response import Response

from recipe.models import Recipe

logger = logging.getLogger(__name__)


class RecipeService:

    @classmethod
    def recipeList(cls, prod_names_list):
        try:
            recipeList = Recipe.objects.all()
            recipe_details = []
            logger.info(f"선택된 제품명: {prod_names_list}")

            # 조건을 만족하는 음식 이름과 관련 재료 정보를 저장
            matching_names = []  # 음식 이름 리스트

            for recipe in recipeList:
                # Convert fields to strings
                food_name = str(recipe.food_name or "").lower()
                material_name = str(recipe.material_name or "")

                # 문자열이 비어있는 경우에는 건너뛰도록 합니다.
                if material_name:
                    # Check if all input words are present in the food name
                    if all(word.lower() in material_name for word in prod_names_list):
                        matching_names.append(food_name)


                        # 새로 추가된 부분: 음식과 관련 재료를 함께 저장
                        recipe_details.append({
                            "recipe_name": food_name,
                            "ingredients": [ingredient.strip() for ingredient in material_name.split(",")]
                        })

            # 최대 5개의 레시피를 랜덤으로 선택
            if recipe_details:
                recipe_details = random.sample(recipe_details, min(5, len(recipe_details)))

            # 결과 출력
            if matching_names:
                # 상위 5개를 랜덤으로 선택
                selected_names = random.sample(matching_names, min(5, len(matching_names)))
                logger.info(f"랜덤으로 선택된 5개의 이름: {selected_names}")
                return recipe_details  # 단순히 데이터를 반환
            else:
                logger.info("조건에 맞는 레시피가 없습니다.")
                return []


        except DatabaseError as e:

            logger.error("레시피 데이터를 가져오는 중 오류가 발생했습니다.", exc_info=True)

            raise DatabaseError("레시피 데이터를 찾을 수 없습니다.") from e


        except Exception as e:

            logger.exception(f"레시피 처리 중 예기치 못한 오류 발생: {e}")

            raise Exception("서버 오류가 발생했습니다.") from e

