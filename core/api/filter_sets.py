import core.models
from django_filters import rest_framework as filters


class CategoryInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class PostFilter(filters.FilterSet):
    categories__in = CategoryInFilter(field_name='categories__name', lookup_expr='in')

    class Meta:
        model = core.models.Post
        fields = ('title', 'is_active', 'author__username', 'author', 'date', 'categories__in')