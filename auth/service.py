import logging

from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from profile.models import Profile
from user.models import User

logger = logging.getLogger(__name__)


class AuthService:
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
                        "user": {"id": profile.user_id, "user_id" : user.user_id, "profile_name": profile.profile_name, "leaderYn" : profile.leader_yn},
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
