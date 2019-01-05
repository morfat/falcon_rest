import importlib
from urllib import parse



def get_module_routes(path,module_name):
    #returns module  wide routes

    urls =  module_name + '.urls' #create full module path for import

    #print (urls, path,module_name)


    module = importlib.import_module(urls) #

    module_routes = module.routes
    routes = []

    for mr in module_routes:
        #print (mr)
        inner_path = path + mr[0]
        route = (inner_path,mr[1]) #full path with view to handle path
        routes.append(route)

    return routes


def get_project_routes(app_routes):
    #return project wide routes

    routes = []

    for module_route_config in app_routes:
        module_routes = get_module_routes(  path = module_route_config[0] , module_name = module_route_config[1])
        #print (module_routes)
        routes.extend(module_routes)

    return routes



def urlpatterns(version,app_routes):
    #return project wide routes

    project_routes = get_project_routes(app_routes)

    routes = []

    for route_config in project_routes:
        path = '/' + version + route_config[0]

        #print (path)

        view_obj = route_config[1]
        route = ( path, view_obj )
        routes.append( route )

    return routes
