import django_filters

from core.serializers.utils import LimitOffsetSerializer


def limit_filter(request, queryset):
    limit_offset_serializer = LimitOffsetSerializer(data=request.GET)
    limit_offset_serializer.is_valid(raise_exception=True)

    limit = limit_offset_serializer.data.get('limit')
    offset = limit_offset_serializer.data.get('offset')

    if (offset, limit) == (None, None):
        start, end = None, None
    elif offset is None:
        start = None
        end = limit
    elif limit is None:
        start = offset
        end = None
    else:
        start = offset
        end = offset + limit

    return queryset[start:end]

class NumberFilterInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass
