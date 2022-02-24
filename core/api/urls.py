from django.urls import path

from core.api import views
from core.api.routers import SimpleRouterOptionalSlash, CustomRouter, MyAccountRouter

custom_router = CustomRouter()
custom_router.register('posts', views.PostViewSet)
custom_router.register('accounts', views.AccountViewSet)
custom_router.register('reactions', views.ReactionsViewSet)
custom_router.register('comments', views.CommentViewSet)
router = SimpleRouterOptionalSlash()
router.register('categories', views.PostCategoryViewSet)

my_account_router = MyAccountRouter()
my_account_router.register('account', views.MyAccountViewSet)

urlpatterns = [
    path('registration/', views.APIRegisterUser.as_view()),
]

urlpatterns += router.urls
urlpatterns += custom_router.urls
urlpatterns += my_account_router.urls