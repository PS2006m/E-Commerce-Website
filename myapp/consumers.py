import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from django.utils.timezone import now

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "general_chat"
        self.room_group_name = f"chat_{self.room_name}"

        # Accept WebSocket connection
        await self.accept()

        # Load previous messages and send to user
        messages = await self.get_previous_messages()
        for message in messages:
            await self.send(text_data=json.dumps({
                "message": message.message,
                "username": message.username,
                "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }))

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        # Save message to the database
        chat_message = ChatMessage(username=username, message=message, timestamp=now())
        await self.save_message(chat_message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))

    async def save_message(self, chat_message):
        """ Save message to the database (runs in sync thread) """
        from asgiref.sync import sync_to_async
        await sync_to_async(chat_message.save)()

    async def get_previous_messages(self):
        """ Retrieve last 20 messages from database """
        from asgiref.sync import sync_to_async
        return await sync_to_async(lambda: ChatMessage.objects.order_by('-timestamp')[:20])()
