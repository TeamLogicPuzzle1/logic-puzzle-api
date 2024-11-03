from django.db import IntegrityError, DatabaseError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class ProfileService:
    def profileSave(data, serializer_class):
        try:
            # 전달받은 데이터를 이용해 serializer 객체 생성
            serializer = serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            profile = serializer.save()
            return Response({"message": "멤버추가가 성공적으로 완료되었습니다.", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # 유효성 검사 실패 시 예외 처리
            return Response({"message": "멤버추가 양식에 맞지않습니다.", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            # 데이터베이스 중복 오류 처리 (예: 이미 존재하는 사용자)
            return Response({"message": "이미 존재하는 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            # 기타 데이터베이스 관련 예외 처리
            return Response({"message": "데이터베이스 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # 기타 예상치 못한 예외 처리
            return Response({"message": f"알 수 없는 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)