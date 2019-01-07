import os
import falcon

from falcon_rest.conf import settings

from falcon_rest.db import models


import importlib
from pydoc import locate

urls_module = importlib.import_module(settings.URLS_MODULE)

def create_db_tables():
    #create all db tables 

    for app in settings.INSTALLED_APPS:
        app_models = app + '.models'
        try:
            importlib.import_module(app_models)
        except ModuleNotFoundError:
            pass
            

    models.Base.metadata.create_all(settings.DB_ENGINE)

def get_wsgi_application():
    #1. Create db tables if not created

    app = falcon.API(media_type='application/json',
                    middleware = [ locate(klass)() for klass in settings.MIDDLEWARE ]
                    )
  
    for route in urls_module.routes:
        app.add_route(*route)

   
    return app
    