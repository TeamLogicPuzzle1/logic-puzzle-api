import logging

from django.contrib.auth.hashers import check_password
from django.db import IntegrityError, DatabaseError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from profile.models import Profile
from user.models import User

logger = logging.getLogger(__name__)


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

    @classmethod
    def login(cls, data, serializer_class):
        serializer = serializer_class(data=data)
        if not serializer.is_valid():
            logger.error(f"Validation Error: {serializer.errors}")  # 유효성 검사 오류 로그 기록
            return Response({"message": "잘못된 요청입니다.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        member_id = serializer.validated_data.get("member_id")
        pin_num = serializer.validated_data.get("pin_num")

        # 데이터베이스에서 member_id로 사용자 검색
        try:
            profile = Profile.objects.get(id=member_id)
            user = User.objects.get(id=profile.user_id)

            # 저장된 핀 번호가 해시되어 있으므로 check_password로 검증
            if check_password(str(pin_num), profile.pin_num):
                # 로그인 성공, 토큰 생성
                refresh = RefreshToken.for_user(user)
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)

                res = Response(
                    {
                        "user": {"id": profile.user_id, "profile_name": profile.profile_name},
                        "message": "login success",
                        "token": {
                            "access": access_token,
                            "refresh": refresh_token,
                        },
                    },
                    status=status.HTTP_200_OK,
                )
                return res
            else:
                logger.error("Authentication failed: Invalid pin number")
                return Response({"message": "로그인 실패: 핀 번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            # 사용자가 존재하지 않는 경우
            logger.error("Authentication failed: User not found")
            return Response({"message": "로그인 실패: 사용자를 찾을 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
