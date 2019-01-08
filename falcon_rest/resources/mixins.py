



class CreateAPIMixin:

    """ 
    Requires
    """

    def create(self, req, session, serialized_data, **kwargs):

        """
        Create record to storage. return newly createed . called for HTTP scenarios
        """

        obj = self.table(**serialized_data)
        session.add(obj)
        return obj
    
class ListAPIMixin:

    def list(self, req, session, **kwargs):
        
        """ select from resource storage and return as list 
        """

        
        filtered_query = self.get_filtered_query(req, session)

        
        return filtered_query.all()


class RetrieveAPIMixin:

    def retrieve(self, req, session, pk, **kwargs):
        
        """ select single  from resource storage and return as list 
        """
        
        return self.get_object(req, session, pk)



class UpdateAPIMixin:

    def update(self, req, session, pk, new_data, **kwargs):
        
        """ 
        Update use PUT
        """
        instance = self.get_object(req, session, pk)

        #session.query(self.table).filter(self.table.id == pk )
        self.get_object_queryset(req, session, pk).update(new_data)

        return instance



class DestroyAPIMixin:

    def destroy(self, req, session, pk, **kwargs):
        
        """ 
        Delete record
        """

        self.get_object_queryset(req, session, pk).delete()
        
        return None
