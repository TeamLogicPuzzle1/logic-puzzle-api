from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from firebase_admin import messaging
from .serializers import NotificationRequestSerializer
from .firebase import firebase_app  # Firebase 초기화

@swagger_auto_schema(
    method='post',
    request_body=NotificationRequestSerializer,
    operation_description="Send a Firebase notification to a device using its token."
)
@api_view(['POST'])
def send_notification(request):
    serializer = NotificationRequestSerializer(data=request.data)

    # 데이터 검증
    if serializer.is_valid():
        title = serializer.validated_data.get('title')
        body = serializer.validated_data.get('body')
        token = serializer.validated_data.get('token')

        # FCM 메시지 생성
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )

        try:
            # Firebase 알림 전송
            response = messaging.send(message)
            return Response({'message': '알림이 전송되었습니다.', 'response': response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)