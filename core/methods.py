from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_notification(notification_type, content):
    channel = get_channel_layer()
    async_to_sync(channel.group_send)(
        "notifications",
        {
            "type": "send_notification",
            "message": {"content": content, "type": notification_type},
        },
    )


def send_chat_message(message, stream_status="on_progress"):
    channel = get_channel_layer()
    async_to_sync(channel.group_send)(
        "chat",
        {
            "type": "send_message",
            "message": {"content": message, "stream_status": stream_status},
        },
    )
