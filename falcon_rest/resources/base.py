from falcon_rest.conf import settings

from sqlalchemy.sql import and_, or_
from sqlalchemy import  literal_column





class Resource:

    """ This is the base resource class. 

    Currently suports Marshmallow serilaizers only.

    Search params example format: ?search=subject__startswith:test3,state__eq:Initial


    """

    table = None
    limit = settings.PAGINATION_PAGE_SIZE
    serializer_class = None
    search_fields = None
    filter_fields = None


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

        
        
    def get_filtered_query(self, req, session):
        #both search and filter are applied to the query as per given GET params
        queryset = self.get_query(session)
        params = req.params


        search_params = params.get(settings.SEARCH_QUERY_PARAM)
        filter_params = params.get(settings.FILTER_QUERY_PARAM)
       

        
        if search_params and self.search_fields:
            queryset = self.search_queryset(queryset, search_params)
        
        if filter_params and self.filter_fields:
            queryset = self.filter_queryset(queryset, filter_params)

        #1. Apply search
        return queryset

        



    def get_object_queryset(self, req, session, pk ):
        
        filtered_query = self.get_filtered_query(req, session)

        #apply pk filtering
        return filtered_query.filter( self.table.id == pk )

    
    def get_object(self, req, session, pk ):

        return self.get_object_queryset(req, session,pk).one()

       






"""
    def get_queryset(self):
        return self.table.__table__.select()

    def insert(self, conn,  data):
        result = conn.execute( self.table.__table__.insert(), **data )
        inserted_pk = result.inserted_primary_key
        return inserted_pk[0]
    
    def fetch(self, conn, search_by=None, filter_by=None, sort_by=None, limit=None, for_update=None):
        limit = limit if limit else self.limit

        queryset = self.get_queryset().limit( limit )
        
        if for_update:
            queryset = queryset.with_for_update()

        return conn.execute( queryset ).fetchall()
    
    def retrieve(self, conn, pk, for_update=None):
        queryset = self.get_queryset().where( self.table.id == pk )
        
        if for_update:
            queryset = queryset.with_for_update()

        result = conn.execute( queryset ).fetchone()
        return dict(result)
    
    def update(self, conn, pk, new_data):
        result = conn.execute( self.table.__table__.update().values( **new_data ).where( self.table.id == pk ) )
        return result
        
    
    def destroy(self, conn, pk):
        queryset = self.table.__table__.delete().where( self.table.id == pk )
        return conn.execute( queryset )


"""



    
    

