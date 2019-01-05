import os
import falcon

from .settings import settings

from falcon_rest.models import Base
from falcon_rest import media

import importlib
from pydoc import locate

urls_module = importlib.import_module(settings.URLS_MODULE)

def create_db_tables():
    #create all db tables 

    for app in settings.INSTALLED_APPS:
        app_models = app + '.models'
        importlib.import_module(app_models)
    
    Base.metadata.create_all(settings.DB_ENGINE)

def get_wsgi_application():
    #1. Create db tables if not created

    app = falcon.API(media_type='application/json',
                    middleware = [ locate(klass)() for klass in settings.MIDDLEWARE ]
                    )
  
    for route in urls_module.routes:
        app.add_route(*route)

    #register the custom handler here
    app.resp_options.media_handlers = handlers

    return app
    