from rest_framework.routers import Route, SimpleRouter


class AccountRouter(SimpleRouter):

    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'

    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'list', 'post': 'create'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/login{trailing_slash}$',
            mapping={'get': 'user_login'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        Route(
            url=r'^{prefix}/logout{trailing_slash}$',
            mapping={'get': 'user_logout'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),

        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={'get': 'retrieve', 'patch': 'partial_update'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
    ]


class CustomRouter(SimpleRouter):

    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'

    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'list', 'post': 'create'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={'get': 'retrieve', 'delete': 'destroy', 'put': 'partial_update'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
    ]


class SimpleRouterOptionalSlash(SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'
