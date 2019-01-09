from ..resources import mixins
from .base import Resource
from  marshmallow import ValidationError
import falcon 

class CreateAPI(Resource, mixins.CreateAPIMixin):

    """ Generic POST """
    
    def on_post(self, req, resp, **kwargs):
        session = req.context['session']
        serializer = self.serializer_class()
        try:
            serialized = serializer.load( req.media )
          
            created_object = self.create(req, session, serialized)

        except ValidationError as err:
            #err.messages
            
            raise falcon.HTTPBadRequest(title='Invalid Data', description=err.messages)


        #serialize for output
        resp_data = serializer.dump( created_object )



        resp.media = { "data": [ resp_data ] }



class ListAPI(Resource, mixins.ListAPIMixin):

    """ Generic GET """
    
    def on_get(self, req, resp, **kwargs):
        session = req.context['session']

        serializer = self.serializer_class(many=True)
        paginator = self.pagination_class()
        
        results = self.list(req, session, paginator)
        serialized = serializer.dump( results )

        response_data = {"data": serialized }

        resp.media = paginator.get_paginated_response(response_data, req)

        

class RetrieveAPI(Resource, mixins.RetrieveAPIMixin):

    """ Generic Single Resource GET """
    
    def on_get(self, req, resp,pk, **kwargs):
        session = req.context['session']

        serializer = self.serializer_class()
        result = self.retrieve(req, session, pk)
        serialized = serializer.dump( result )
        
        resp.media = {"data": [ serialized ]}


            
class UpdateAPI(Resource, mixins.UpdateAPIMixin):

    """ Generic Single Resource PUT """
    
    def on_put(self, req, resp, pk, **kwargs):
        session = req.context['session']

        serializer = self.serializer_class()

        try:
            req_serialized = serializer.load( req.media )
            updated = self.update(req, session, pk, req_serialized)

        except ValidationError as err:
            #err.messages
            
            raise falcon.HTTPBadRequest(title='Invalid Data', description=err.messages)

        
        #serialize for output
        resp_serialized = serializer.dump( updated )

        resp.media = {"data": [ resp_serialized ]}

class DestroyAPI(Resource, mixins.DestroyAPIMixin):

    """ Generic Destroy"""
    
    def on_delete(self, req, resp, pk, **kwargs):
        session = req.context['session']
        self.destroy(req, session, pk)
        resp.media = {"data": [ None ]}

        
        
class ListCreateAPI(ListAPI, CreateAPI ):
    pass

class RetrieveUpdateAPI(RetrieveAPI, UpdateAPI):
    pass

class RetrieveDestroyAPI(RetrieveAPI, DestroyAPI):
    pass

class RetrieveUpdateDestroyAPI(RetrieveAPI, UpdateAPI, DestroyAPI):
    pass



