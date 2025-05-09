import django_filters

from .models import MenuItem


class MenuItemFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(choices=MenuItem.Category.choices)

    class Meta:
        model = MenuItem
        fields = ["category"]
