import json  
  
from channels.generic.websocket import AsyncWebsocketConsumer  
from chats.tasks import process_chat
from rich import print
from core.ai.prompt_manager import PromptManager

  
class NotificationConsumer(AsyncWebsocketConsumer):  
    async def connect(self):  
        await self.accept()  
        await self.channel_layer.group_add("notifications", self.channel_name)  
  
    async def disconnect(self, close_code):  
        await self.channel_layer.group_discard("notifications", self.channel_name)  
  
    async def send_notification(self, event):  
        message = event["message"]  
        await self.send(text_data=json.dumps({"message": message}))

class ChatConsumer(AsyncWebsocketConsumer):  
    async def connect(self):
        self.group_name = "chat"

        await self.accept()  
        await self.channel_layer.group_add(self.group_name, self.channel_name)  
  
    async def disconnect(self, close_code):  
        await self.channel_layer.group_discard(self.group_name, self.channel_name)  
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        process_chat(message)

    async def send_message(self, event):  
        message = event["message"]  
        await self.send(text_data=json.dumps({"message": message}))