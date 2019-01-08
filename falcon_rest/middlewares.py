#from falcon_rest.auth import auth
from falcon_rest.conf import settings
import falcon

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=settings.DB_ENGINE)

class CoreMiddleWare:
    
    def process_request(self,req,resp):
        req.context['session'] = Session()

    def process_response(self,req,resp,resource,req_succeeded):
        try:
            if req_succeeded:
                req.context['session'].commit()
            else:
                req.context['session'].rollback()
        except:
            pass
        finally:
            req.context['session'].close()


class CORSMiddleWare:
    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin','*')
        if (req.method == 'OPTIONS' and req.get_header('Access-Control-Request-Method')): #req_succeeded and 
            #preflight CORS request

            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header(
                'Access-Control-Request-Headers', default='*'
            )

            resp.set_headers((
                ('Access-Control-Allow-Methods', allow),
                ('Access-Control-Allow-Headers', allow_headers),
                ('Access-Control-Max-Age', '86400'),  # 24 hours
            ))



"""
class AuthMiddleWare:
        
    def process_resource(self,req,resp,resource,params):
        
        if req.method != 'OPTIONS':
            
            must_login = True
            auth_token_type = 'Bearer'

            try:
                must_login = resource.login_required #we expect login_required = False
            except AttributeError:
                pass
            
            try:
                auth_token_type = resource.auth_token_type #we expect login_required = False
            except AttributeError:
                pass
                

            if must_login:
                auth_data = None

                if auth_token_type == 'Bearer':
                    

                    auth_data = auth.validate_jwt_token( bearer_token = req.auth)
                    
                if auth_data is None:
                    raise falcon.HTTPUnauthorized(description = 'Login Required')
                
                req.context['auth'] = auth_data
             
    def get_secret_key(self,req):
        return self.secret_key
"""