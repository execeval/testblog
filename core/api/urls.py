
from core.api import views
from core.api.routers import SimpleRouterOptionalSlash, CustomRouter, AccountRouter

custom_router = CustomRouter()
custom_router.register('posts', views.PostViewSet)
custom_router.register('reactions', views.ReactionsViewSet)
custom_router.register('comments', views.CommentViewSet)

account_router = AccountRouter()
account_router.register('accounts', views.AccountViewSet)

router = SimpleRouterOptionalSlash()
router.register('categories', views.PostCategoryViewSet)

urlpatterns = [
]

urlpatterns += router.urls
urlpatterns += custom_router.urls
urlpatterns += account_router.urls