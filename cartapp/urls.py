from django.urls import path
from . import views,views_auth

urlpatterns = [
    path('login/',views_auth.login_api),
    path('user/',views_auth.get_user_data),
    path('register/',views_auth.register_api),
    path('logout/',views_auth.user_logout),
]