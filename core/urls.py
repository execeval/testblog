from django.contrib import admin
from django.urls import path, include
import core.views as views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Main.as_view(), name='home'),
    path('api/', include('core.api.urls')),
    path('register/', views.Registration.as_view(), name='register'),
    path('actions/registration/', views.registration_post_form, name='post_url_registration'),
    path('logout/', views.logout_post, name='logout'),
    path('auth/', views.LoginView.as_view(), name='auth'),
    path('actions/auth/', views.login_post, name='post_url_login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)