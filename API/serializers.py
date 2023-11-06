from rest_framework import serializers


class VideoSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    url = serializers.URLField(required=False)