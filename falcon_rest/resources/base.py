from falcon_rest.conf import settings

from sqlalchemy.sql import and_, or_
from sqlalchemy import  literal_column
import sqlalchemy as sa

from falcon_rest.paginators import PageNumberPagination
import falcon 


class Resource:

    """ This is the base resource class. 

    Currently suports Marshmallow serilaizers only.

    Search params example format: ?search=subject__startswith:test3,state__eq:Initial



    """

    table = None
    limit = settings.PAGINATION_PAGE_SIZE
    serializer_class = None
    pagination_class = PageNumberPagination

    search_fields = None
    filter_fields = None
    ordering_fields = ['id']
    ordering = 'id:desc' #of default fields for ordering if none specified


    def map_column_filter(self, column, action, value):
        #example input => ('name', 'contains','mosoti',)
        

        col = literal_column( column ) #to sqlalchemy column

        ops_dict = {
            'startswith':col.startswith(value),
            'endswith': col.endswith(value),
            'contains': col.contains(value),
            'eq': col.op("=")(value),
            'lt': col.op("<")(value),
            'lte': col.op("<=")(value),
            'gt': col.op(">")(value),
            'gte': col.op(">=")(value)
        }
    
        return ops_dict[action]
    
   

    def get_query(self, session):
        return session.query( self.table)
    
   
    def filter_queryset(self, queryset, filter_params):
        try:
            filter_params = filter_params.split() #some params come as one string
        except AttributeError:
            pass

        #make filters
        filters = []
        for sp in filter_params:
            col_action, value = sp.split(':')
            column, action = col_action.split('__') #this is double underscore

            if column in self.filter_fields:
                filters.append( self.map_column_filter( column, action, value ) )
        
        #apply filters
        return queryset.filter(
            and_(
                *filters
             )
            )

    
    def search_queryset(self, queryset, search_params):
        try:
            search_params = search_params.split() #some params come as one string
        except AttributeError:
            pass

        #make filters
        filters = []
        for sp in search_params:
            col_action, value = sp.split(':')
            column, action = col_action.split('__') #this is double underscore

            if column in self.search_fields:
                filters.append( self.map_column_filter( column, action, value ) )
        
        #apply filters
        return queryset.filter(
            or_(
                *filters
             )
            )
    
    def order_queryset(self, queryset, req):
        params = req.params
        ordering_params = params.get(settings.ORDERING_QUERY_PARAM)
        try:
            ordering_params = ordering_params.split() #some come as string
        except AttributeError:
            pass

        if not ordering_params:
            #apply default ordering
            ordering = self.ordering
            ordering_params = ordering.split()
        
        for op in ordering_params:
            col,style = op.split(':')
            if col in self.ordering_fields:
                if style == 'desc':
                    queryset = queryset.order_by( literal_column(col).desc() )
                elif style == 'asc':
                    queryset = queryset.order_by( literal_column(col).asc() )
        
        return queryset



                

        



        
        
    def get_filtered_query(self, session, req=None):
        #both search and filter are applied to the query as per given GET params
       
        queryset = self.get_query(session)
        if not req:
            return queryset

        params = req.params


        search_params = params.get(settings.SEARCH_QUERY_PARAM)
        filter_params = params.get(settings.FILTER_QUERY_PARAM)
       

        
        if search_params and self.search_fields:
            queryset = self.search_queryset(queryset, search_params)
        
        if filter_params and self.filter_fields:
            queryset = self.filter_queryset(queryset, filter_params)

        #1. Apply search
        return queryset

        



    def get_object_queryset(self, session, pk , req=None):
        
        filtered_query = self.get_filtered_query(session, req)

        #apply pk filtering
        return filtered_query.filter( self.table.id == pk )

    
    def get_object(self, session, pk , req=None):
        try:
            return self.get_object_queryset(session,pk, req).one()
        except sa.orm.exc.NoResultFound:
            raise falcon.HTTPNotFound( description="The requested record doesnot exist")


       





