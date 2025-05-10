import django_filters
import pytz
from datetime import datetime, time
from django.conf import settings
from django.utils import timezone

from .models import Order


class OrderFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(method='filter_by_date')
    
    def filter_by_date(self, queryset, name, value):
        # Get the timezone from settings
        local_tz = pytz.timezone(settings.TIME_ZONE)
        
        # Create datetime objects for the start and end of the selected date in local timezone
        start_datetime = datetime.combine(value, time.min)
        end_datetime = datetime.combine(value, time.max)
        
        # Localize the datetime objects to the local timezone
        start_datetime = local_tz.localize(start_datetime)
        end_datetime = local_tz.localize(end_datetime)
        
        # Convert to UTC for database query if USE_TZ is True
        if settings.USE_TZ:
            start_datetime = start_datetime.astimezone(pytz.UTC)
            end_datetime = end_datetime.astimezone(pytz.UTC)
        
        # Filter orders between start and end of the selected date
        return queryset.filter(date__gte=start_datetime, date__lte=end_datetime)
    
    class Meta:
        model = Order
        fields = ["date"]
