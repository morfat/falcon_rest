from falcon_rest.conf import settings


class Resource:

    """ This is the base resource class. 

    Currently suports Marshmallow serilaizers only.
    
    """

    table = None
    limit = settings.PAGINATION_PAGE_SIZE
    serializer_class = None

    def get_query(self, session):
        return session.query( self.table)
    
    def get_filtered_query(self, req, session):
        return self.get_query(session)




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



    
    

