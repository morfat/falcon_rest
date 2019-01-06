from ..resources import mixins
from .base import Resource

class InsertAPI(Resource, mixins.InsertAPIMixin):

    """ Generic POST """
    
    def on_post(self, req, resp, **kwargs):
        conn = req.context['connection']
        serialized_data = req.media
        resp.media = self.perform_insert(req, conn, serialized_data)

class FetchAPI(Resource, mixins.FetchAPIMixin):

    """ Generic GET """
    
    def on_get(self, req, resp, **kwargs):
        conn = req.context['connection']
        resp.media = self.perform_fetch(req, conn)

class RetrieveAPI(Resource, mixins.RetrieveAPIMixin):

    """ Generic Single Resource GET """
    
    def on_get(self, req, resp,pk, **kwargs):
        conn = req.context['connection']
        resp.media = self.perform_retrieve(req, conn, pk)

class FetchRetrieveAPI(Resource, mixins.FetchAPIMixin, mixins.RetrieveAPIMixin):

    """ Generic GET list or retrieve one """
    
    def on_get(self, req, resp, pk=None, **kwargs):
        conn = req.context['connection']
        if pk:
            resp.media = self.perform_retrieve(req, conn, pk)
        else:
            resp.media = self.perform_fetch(req, conn)


class UpdateAPI(Resource, mixins.UpdateAPIMixin):

    """ Generic Single Resource PUT """
    
    def on_put(self, req, resp, pk, **kwargs):
        conn = req.context['connection']
        new_data = req.media
        resp.media = self.perform_update(req, conn, pk, new_data)

class DestroyAPI(Resource, mixins.DestroyAPIMixin):

    """ Generic Destroy"""
    
    def on_delete(self, req, resp, pk, **kwargs):
        conn = req.context['connection']
        self.perform_destroy(req, conn, pk)
        resp.media = {}
        
        

class GenericAPI(InsertAPI, FetchRetrieveAPI, UpdateAPI, DestroyAPI):
    pass
