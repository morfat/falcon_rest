



class InsertAPIMixin:

    """ Requires base class that implements the called methods 
    insert()
    """

    def perform_insert(self, req, conn, serialized_data, **kwargs):
        """ Insert record to storage. return newly inserted . called for HTTP scenarios"""
        resp_data = self.insert(conn, serialized_data)
        return { "data": [ resp_data ]  }
    
class FetchAPIMixin:

    def perform_fetch(self, req, conn, search_by=None, filter_by=None, order_by=None, **kwargs):
        
        """ select from resource storage and return as list 
        """
        resp_data =  self.fetch(conn, search_by, filter_by, order_by)
        return { "data": [ dict(row) for row in resp_data ]  }


class RetrieveAPIMixin:

    def perform_retrieve(self, req, conn, pk, **kwargs):
        
        """ select single  from resource storage and return as list 
        """
        
        resp_data =  self.retrieve(conn, pk)
        return { "data": [ resp_data ]  }


class UpdateAPIMixin:

    def perform_update(self, req, conn, pk, new_data, **kwargs):
        
        """ Update use PUT
        """
        
        self.update(conn, pk, new_data)
        
        resp_data = self.retrieve(conn, pk)

        return resp_data


class DestroyAPIMixin:

    def perform_destroy(self, req, conn, pk, **kwargs):
        
        """ Delete record
        """
        
        resp_data =  self.destroy(conn, pk)
        return None
