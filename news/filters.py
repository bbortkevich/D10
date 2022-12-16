import django_filters
from .models import Post
import django.forms

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title', label='Заголовок содержит', lookup_expr='icontains',
        widget=django.forms.TextInput(
            attrs={'type': 'text', 'class': "form-control", 'placeholder': "Ведите текст..."}))

    date_time__gt = django_filters.DateFilter(
        field_name="date", label="Не ранее даты", lookup_expr='gt',
        widget=django.forms.DateInput(
            attrs={'type': 'date', 'class': "form-control"}))

    class Meta:
        model = Post
        fields = ['title', 'author', 'date_time__gt']
