from django.db.models import QuerySet


def get_by_filter(queryset: QuerySet, **kwargs) -> QuerySet:
    qs = queryset
    search = kwargs.get("search")

    if search:
        qs = qs.filter(description__icontains=search)

    return qs.order_by("-created_at")
