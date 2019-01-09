



class CreateAPIMixin:

    """ 
    Requires
    """

    def create(self, req, session, serialized_data, **kwargs):

        """
        Create record to storage. return newly createed . called for HTTP scenarios
        """

        #obj = self.table(**serialized_data)
        # result = session.add(obj)
        created_data = self.perfom_create(session, serialized_data)

        #get object inserted for representation
        obj = self.get_object(session, pk=created_data.get("id"))
        return obj
    
    def perfom_create(self, session, serialized_data):
        result = session.execute( self.table.__table__.insert(), serialized_data)
        inserted_pk = result.inserted_primary_key[0]

        serialized_data.update({ "id": inserted_pk })
        return serialized_data



    
class ListAPIMixin:

    def list(self, req, session, paginator, **kwargs):
        
        """ select from resource storage and return as list 
        """

      
        filtered_query = self.get_filtered_query(session, req)
        ordered_queryset = self.order_queryset( queryset=filtered_query, req=req)

        paginated_queryset = paginator.paginate_queryset(ordered_queryset, req)

        
        return paginated_queryset.all()


class RetrieveAPIMixin:

    def retrieve(self, req, session, pk, **kwargs):
        
        """ select single  from resource storage and return as list 
        """
        
        return self.get_object(session, pk, req)



class UpdateAPIMixin:

    def update(self, req, session, pk, new_data, **kwargs):
        
        """ 
        Update use PUT
        """
        instance = self.get_object(session, pk, req)

        #session.query(self.table).filter(self.table.id == pk )
        self.get_object_queryset(session, pk, req).update(new_data)

        return instance



class DestroyAPIMixin:

    def destroy(self, req, session, pk, **kwargs):
        
        """ 
        Delete record
        """

        self.get_object_queryset(session, pk, req).delete()
        
        return None
