from rest_framework.routers import Route, SimpleRouter


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


class MyAccountRouter(SimpleRouter):

    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'

    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'retrieve', 'post': 'create', 'delete': 'destroy', 'put': 'partial_update'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        )
    ]
