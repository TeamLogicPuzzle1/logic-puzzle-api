from rest_framework.views import APIView
from rest_framework.response import Response
from .fcm import send_fcm_message

class NotificationSendView(APIView):
    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        body = request.data.get('body')
        token = request.data.get('token')

        fcm_response = send_fcm_message(token, title, body)

        return Response({
            'message': 'Notification sent.',
            'fcm_response': fcm_response
        })