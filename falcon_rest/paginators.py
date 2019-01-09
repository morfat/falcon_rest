
from falcon_rest.conf import settings

from urllib import parse


def replace_query_param(url, key, val):
    """
    Given a URL and a key/val pair, set or replace an item in the query
    parameters of the URL, and return the new URL.
    """
    (scheme, netloc, path, query, fragment) = parse.urlsplit(url)
    query_dict = parse.parse_qs(query, keep_blank_values=True)
    query_dict[str(key)] = [val]
    query = parse.urlencode(sorted(list(query_dict.items())), doseq=True)
    return parse.urlunsplit((scheme, netloc, path, query, fragment))

def remove_query_param(url, key):
    """
    Given a URL and a key/val pair, remove an item in the query
    parameters of the URL, and return the new URL.
    """
    (scheme, netloc, path, query, fragment) = parse.urlsplit(url)
    query_dict = parse.parse_qs(query, keep_blank_values=True)
    query_dict.pop(key, None)
    query = parse.urlencode(sorted(list(query_dict.items())), doseq=True)
    return parse.urlunsplit((scheme, netloc, path, query, fragment))



class BasePagination(object):
   
    def paginate_queryset(self, queryset, req):
        raise NotImplementedError('paginate_queryset() must be implemented.')

    def get_paginated_response(self, resp_data, req):
        raise NotImplementedError('get_paginated_response() must be implemented.')

 

class PageNumberPagination(BasePagination):
    """
    A simple page number based style that supports page numbers as
    query parameters. For example:
    http://api.example.org/accounts/?page=4
    http://api.example.org/accounts/?page=4&page_size=100
    """
    # The default page size.
    # Defaults to `None`, meaning pagination is disabled.
    page_size = settings.PAGINATION_PAGE_SIZE

    # Client can control the page using this query parameter.
    page_query_param = 'page'
  
    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = 'page_size'
  
    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = 10000

    
    def get_page_size(self, request_params):
        page_size = request_params.get(self.page_size_query_param, self.page_size)
        return int(page_size)

    
    def get_page_number(self, request_params):
        page = request_params.get( self.page_query_param , 1 )
        return int(page)


    def paginate_queryset(self, queryset, req):
        request_params = req.params 

        
        page_size = self.get_page_size(request_params) 
        page_number = self.get_page_number(request_params)

        offset = ( page_number - 1 ) * page_size
        limit = page_size

        return queryset.limit( limit ).offset( offset )
    
    def get_next_url(self, url, results_count, current_page_size, current_page_number):
        if results_count >= current_page_size:
            next_page = current_page_number + 1
            url = replace_query_param(url, self.page_query_param, next_page)
        else:
            url = None

        return url
    
    def get_prev_url(self, url, results_count, current_page_size, current_page_number):
        prev_page = current_page_number - 1
        if prev_page <2:
            url = None
        else:
            url = replace_query_param(url, self.page_query_param, prev_page)
        
        return url


    def get_paginated_response(self, response_data, req):
        request_params = req.params 
        results = response_data['data']
        url = req.uri
        
        results_count = len(results)
        page_size = self.get_page_size(request_params) 
        page_number = self.get_page_number(request_params)

        next_url = self.get_next_url( url, results_count, page_size, page_number)
        prev_url = self.get_prev_url( url, results_count, page_size, page_number)

        pagination = {"next_url": next_url, "prev_url": prev_url}

        response_data.update({"pagination": pagination})

        return response_data











    