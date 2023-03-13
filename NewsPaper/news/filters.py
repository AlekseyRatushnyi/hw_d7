from django.forms import DateInput
from django_filters import FilterSet, DateFilter
from .models import Post, Author


class PostFilter(FilterSet):
    date = DateFilter(field_name='time_create', widget=DateInput(attrs={'type': 'date'}), label='Поиск по дате публикации',
                      lookup_expr='date__gte')

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author__user__username': ['iexact'],
        }