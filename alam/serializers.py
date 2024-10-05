from rest_framework import serializers

class NotificationRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    body = serializers.CharField()
    token = serializers.CharField()