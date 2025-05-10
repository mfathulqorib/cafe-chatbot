import bson
import pytz
from datetime import datetime

def generate_id():
    return str(bson.ObjectId())


def format_currency(value):
    return f"IDR {value:,.0f}"


def format_datetime(value):
    """Convert UTC datetime to Asia/Jakarta timezone (UTC+7) and format it."""
    jakarta_tz = pytz.timezone("Asia/Jakarta")
    return value.astimezone(jakarta_tz).strftime("%d %B, %Y %H:%M")

def format_asia_jakarta_datetime(value):
    jakarta_tz = pytz.timezone("Asia/Jakarta")
    return value.astimezone(jakarta_tz).strftime("%Y-%m-%d %H:%M")
    
def get_datetime_now():
    return datetime.now(pytz.timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M")
