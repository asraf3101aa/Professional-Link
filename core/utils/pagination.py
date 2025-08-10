from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100
    def get_paginated_response(self, data):
        '''
        Generates a paginated API response by combining input data with pagination metadata,
        including page size, page count, total count, previous, current, and next page numbers.
        '''
        meta = {
            'page_number':self.page.number,
            'page_size': self.page_size,
            'page_count': self.page.paginator.num_pages,
            'total_items':self.page.paginator.count,
            'has_previous_page': self.page.has_previous(),
            'has_next_page': self.page.has_next(),
            'previous_page_url': self.get_previous_link(),
            'next_page_url': self.get_next_link(),
        }

        # Create a paginated response dictionary with 'meta' as the initial key
        paginated_response = {'meta': meta}
        # Copy data from the input dictionary to the paginated response
        for key in data:
            paginated_response[key] = data[key]

        return paginated_response