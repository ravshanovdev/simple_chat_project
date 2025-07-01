import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .models import Message


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type", 'text')  # default text

        content = text_data_json.get('message', '')
        sticker_url = text_data_json.get('sticker', None)

        event_data = {
            'type': 'chat.message',
            'message_type': message_type,
            'message': content,
            'sticker_url': sticker_url
        }

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, event_data)

    async def chat_message(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message_type': event['message_type'],
            "message": event['message'],
            'sticker_url': event.get('sticker_url', '')
        }))


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.other_username = self.scope['url_route']['kwargs']['username']

        if not self.user.is_authenticated or not await self.is_valid_pair(self.user, self.other_username):
            await self.close()
            return

        usernames = sorted([self.user.username, self.other_username])
        self.room_name = f"private_{usernames[0]}_{usernames[1]}"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        message = await Message.objects.acreate(sender=self.user, sender2=self.other_username, room_name=self.room_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        message_type = data.get('type', 'text')  # default text
        content = data.get('message', '')
        sticker_url = data.get('sticker', None)
        audio = data.get('audio', None)

        event_data = {
            'type': 'chat.message',
            'message_type': message_type,
            'message': content,
            'sticker_url': sticker_url,
            'sender': self.user.username,
            'audio': audio
        }

        await self.channel_layer.group_send(self.room_group_name, event_data)
        update_message = await Message.objects.filter(
            sender=self.user,
            room_name=self.room_name
        ).aorder_by('-created_at').afirst()

        if update_message:
            update_message.content = content
            update_message.sticker_url = sticker_url
            update_message.message_type = message_type
            update_message.audio_file = audio  # diqqat: fayl emas, string bo‘lsa ishlamaydi
            await database_sync_to_async(update_message.save)()

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': event['message_type'],
            "message": event['message'],
            'sender': event['sender'],
            'sticker_url': event.get('sticker_url', '')
        }))

    @staticmethod
    async def is_valid_pair(user1, user2):
        return True
