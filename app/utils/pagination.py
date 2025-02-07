from rest_framework import pagination

class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'pagesize'
    page_query_param = 'page'
