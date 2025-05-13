from django.shortcuts import render
from django.http import HttpResponse
from .models import Message, Sticker
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated


def index_view(request):
    return render(request, "index.html")


def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})


def private_index(request):
    if not request.user.is_authenticated:
        return HttpResponse("royxatdan otish kerak.!")
    return render(request, 'private_index.html')


def private_chat(request, username):
    if not request.user.is_authenticated:
        return HttpResponse("royxatdan otish kerak.!")
    return render(request, 'private_chat.html', {'username': username})


class UploadAudioAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        audio_file = request.FILES.get('audio')
        room_name = request.data.get('room')

        message = Message.objects.create(
            sender=request.user,
            room_name=room_name,
            audio_file=audio_file,
            message_type=Message.AUDIO

        )

        return Response({
            'status': 'success',
            'audio_url': message.audio_file.url,
            'room_name': room_name,
            'message_type': 'audio'
        })
