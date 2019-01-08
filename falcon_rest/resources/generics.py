from ..resources import mixins
from .base import Resource

class InsertAPI(Resource, mixins.InsertAPIMixin):

    """ Generic POST """
    
    def on_post(self, req, resp, **kwargs):
        session = req.context['session']
        serialized_data = req.media
        resp.media = self.perform_insert(req, session, serialized_data)

class FetchAPI(Resource, mixins.FetchAPIMixin):

    """ Generic GET """
    
    def on_get(self, req, resp, **kwargs):
        session = req.context['session']
        resp.media = self.perform_fetch(req, session)

class RetrieveAPI(Resource, mixins.RetrieveAPIMixin):

    """ Generic Single Resource GET """
    
    def on_get(self, req, resp,pk, **kwargs):
        session = req.context['session']
        resp.media = self.perform_retrieve(req, session, pk)

class FetchRetrieveAPI(Resource, mixins.FetchAPIMixin, mixins.RetrieveAPIMixin):

    """ Generic GET list or retrieve one """
    
    def on_get(self, req, resp, pk=None, **kwargs):
        session = req.context['session']
        if pk:
            resp.media = self.perform_retrieve(req, session, pk)
        else:
            resp.media = self.perform_fetch(req, session)


class UpdateAPI(Resource, mixins.UpdateAPIMixin):

    """ Generic Single Resource PUT """
    
    def on_put(self, req, resp, pk, **kwargs):
        session = req.context['session']
        new_data = req.media
        resp.media = self.perform_update(req, session, pk, new_data)

class DestroyAPI(Resource, mixins.DestroyAPIMixin):

    """ Generic Destroy"""
    
    def on_delete(self, req, resp, pk, **kwargs):
        session = req.context['session']
        self.perform_destroy(req, session, pk)
        resp.media = {}
        
        

class GenericAPI(InsertAPI, FetchRetrieveAPI, UpdateAPI, DestroyAPI):
    pass
