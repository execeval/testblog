
from core.api import views
from core.api.routers import SimpleRouterOptionalSlash, PostRouter, AccountRouter, CommentariesReactionsRouter

posts_router = PostRouter()

posts_router.register('posts', views.PostViewSet)

commentaries_reactions_router = CommentariesReactionsRouter()

commentaries_reactions_router.register('reactions', views.ReactionsViewSet)
commentaries_reactions_router.register('comments', views.CommentViewSet)

account_router = AccountRouter()
account_router.register('accounts', views.AccountViewSet)

router = SimpleRouterOptionalSlash()
router.register('categories', views.PostCategoryViewSet)

urlpatterns = [
]

urlpatterns += router.urls
urlpatterns += posts_router.urls
urlpatterns += account_router.urls
urlpatterns += commentaries_reactions_router.urls