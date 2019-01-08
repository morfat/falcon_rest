



class InsertAPIMixin:

    """ 
    Requires base class that implements the called methods 
    insert()
    """

    def perform_insert(self, req, session, serialized_data, **kwargs):

        """
        Insert record to storage. return newly inserted . called for HTTP scenarios
        """

        obj = self.table(**serialized_data)
        session.add(obj)
        session.commit()

        return { "data": [ obj ]  }
    
class FetchAPIMixin:

    def perform_fetch(self, req, session,**kwargs):
        
        """ select from resource storage and return as list 
        """

        serializer = self.serializer_class(many=True)

        filtered_query = self.get_filtered_query(req, session)

        
        serialized_data = serializer.dump( filtered_query.all() )
        print(serialized_data)

       
        return { "data": serialized_data.data  }


class RetrieveAPIMixin:

    def perform_retrieve(self, req, session, pk, **kwargs):
        
        """ select single  from resource storage and return as list 
        """
        serializer = self.serializer_class()
        filtered_query = self.get_filtered_query(req, session)

        #apply pk filtering
        row = filtered_query.filter( self.table.id == pk ).one()
        
        #serialize
        serialized_data = serializer.dump( row )
      
        return { "data": [ serialized_data.data ]  }


class UpdateAPIMixin:

    def perform_update(self, req, session, pk, new_data, **kwargs):
        
        """ Update use PUT
        """
        
        self.update(session, pk, new_data)
        
        resp_data = self.retrieve(session, pk)

        return { "data": [ resp_data ]  }


class DestroyAPIMixin:

    def perform_destroy(self, req, session, pk, **kwargs):
        
        """ Delete record
        """
        
        resp_data =  self.destroy(session, pk)
        return None
