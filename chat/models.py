from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    TEXT = 'text'
    AUDIO = 'audio'
    STICKER = 'sticker'

    MESSAGE_TYPES = [
        (TEXT, 'Text'),
        (AUDIO, 'Audio'),
        (STICKER, 'Sticker'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sender2 = models.CharField(max_length=150)
    room_name = models.CharField(max_length=255)  # group or private room
    content = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='chat_audios/', blank=True, null=True)
    sticker_url = models.URLField(blank=True, null=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default=TEXT)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} - {self.message_type} - {self.timestamp}'


class Sticker(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='stickers/')

    def __str__(self):
        return self.name


