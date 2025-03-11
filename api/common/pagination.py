
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from django.core.paginator import InvalidPage, EmptyPage
from rest_framework.response import Response

class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    page_query_param = "page"
    total_count=None

    def paginate_queryset(self, queryset, request: Request, view=None):
        self.total_count=getattr(view, "total_count",None)
        all_requested = request.query_params.get("all", "").lower() in ["true", "1", "yes"]
        self.page_size = (queryset.count() or self.page_size) if all_requested else (self.get_page_size(request) or self.page_size)
        paginator = self.django_paginator_class(queryset, self.page_size)
        page_number = self.get_page_number(request, paginator) or 1
        try:
            self.page = paginator.page(page_number)
        except (InvalidPage, EmptyPage):
            self.page = paginator.page(paginator.num_pages)
        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        return Response({
            "results": data,
            "groupCount": self.page.paginator.count,
            "totalCount":self.total_count if self.total_count else  self.page.paginator.count
        })