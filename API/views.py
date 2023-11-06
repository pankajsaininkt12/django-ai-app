from rest_framework.views import APIView
from django.http.response import JsonResponse
from API.models import *
from API.serializers import *
from API.video_summary import get_summary
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
class ai_video_summary(APIView):
    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not serializer.validated_data.get('file') and not serializer.validated_data.get('url'):
            return JsonResponse({
                'status': 400,
                'message': 'Please enter url or select video.',
                'data': None})
        file = serializer.validated_data.get('file')
        url = serializer.validated_data.get('url')
        if file:
            file_storage = FileSystemStorage()
            filename = file_storage.save(fr"static\video\{file.name}", file)
            summary = get_summary(file=filename)
            # delete audio files
            files = os.listdir(fr'static\audio-chunks')
            for file in files:
                file_path = os.path.join(fr'static\audio-chunks', file)
                os.remove(file_path)
            # delete audio files
            files = os.listdir(fr'static\audio')
            for file in files:
                file_path = os.path.join(fr'static\audio', file)
                os.remove(file_path)
            # delete video files
            files = os.listdir(fr'static\video')
            for file in files:
                file_path = os.path.join(fr'static\video', file)
                os.remove(file_path)
        else:
            summary = get_summary(url=url)
            # delete audio-chunks files
            files = os.listdir(fr'static\audio-chunks')
            for file in files:
                file_path = os.path.join(fr'static\audio-chunks', file)
                os.remove(file_path)
            # delete audio files
            files = os.listdir(fr'static\audio')
            for file in files:
                file_path = os.path.join(fr'static\audio', file)
                os.remove(file_path)
            # delete video files
            files = os.listdir(fr'static\video')
            for file in files:
                file_path = os.path.join(fr'static\video', file)
                os.remove(file_path)
        return JsonResponse({
            'status': 200,
            'message': 'Success',
            'data': {'summary': summary}})