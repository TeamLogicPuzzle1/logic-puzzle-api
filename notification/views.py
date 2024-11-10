# views.py
from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serviceslayer import initialize_firebase, send_push_notification

# Firebase 초기화 (앱 시작 시 한 번만 호출되도록)
initialize_firebase()


@swagger_auto_schema(
    method='post',
    operation_description="Send push notification to a specific device",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING, description='FCM device token', required=True),
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Notification title', required=True),
            'body': openapi.Schema(type=openapi.TYPE_STRING, description='Notification body', required=True),
        },
        required=['token', 'title', 'body'],
    ),
    responses={200: 'Notification sent successfully', 400: 'Error in request'}
)
@api_view(['POST'])
def send_notification_view(request):
    token = request.data.get("token")
    title = request.data.get("title", "Default Title")
    body = request.data.get("body", "Default Body")

    if not token:
        return JsonResponse({"status": "error", "message": "Token is required"}, status=400)

    try:
        send_push_notification(token, title, body)
        return JsonResponse({"status": "success", "message": "Notification sent!"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)