import bson


def generate_id():
    return str(bson.ObjectId())


def format_currency(value):
    return f"IDR {value:,.0f}"
