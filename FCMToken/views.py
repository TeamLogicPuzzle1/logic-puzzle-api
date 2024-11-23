from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from your_app.models import User, Profile  # 기존 User와 Profile을 import
from .models import FCMToken
from .serializers import FCMTokenSerializer

class SaveFCMTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 클라이언트에서 user_id, profile_id, device_number, fcm_token 정보를 전송합니다.
        data = request.data

        try:
            # user_id를 기준으로 User 모델에서 사용자 찾기
            user = User.objects.get(user_id=data.get('user_id'))
            # profile_id와 user를 기준으로 Profile 모델에서 프로필 찾기
            profile = Profile.objects.get(id=data.get('profile_id'), user=user)

            # 해당 사용자의 프로필 및 기기에 대한 FCM 토큰 정보를 저장하거나 갱신
            fcm_token, created = FCMToken.objects.update_or_create(
                user=user,
                profile=profile,
                device_number=data.get('device_number'),
                defaults={'token': data.get('fcm_token')}
            )

            if created:
                return Response({"message": "FCM 토큰이 새로 저장되었습니다."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "FCM 토큰이 갱신되었습니다."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "해당 사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Profile.DoesNotExist:
            return Response({"error": "해당 프로필을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)