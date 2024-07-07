"""cart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from cartapp import views,views_auth,views_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index,name="Home"),
    path('search/', views.search_product, name="Search"),
    
    path('detail/<int:prod_id>/', views.detail),
    path('addtocart/<str:ctype>/', views.addtocart),
    path('addtocart/<str:ctype>/<int:productid>/', views.addtocart),
  
    path('cart/remove_from_cart/<int:productid>/',views.remove_from_cart, name="remove_from_cart"),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
    path('cart/', views.cart,name="Cart"),
    path('cartorder/', views.cartorder, name="CartOrder"),

    
    path('sign_up/',views_auth.sign_up,name='Register'),
    path('login/',views_auth.sign_in,name='Login'),
    path('logout/',views_auth.user_logout,name='Logout'),
    
    path('profile/<int:pk>/',views_profile.profile,name='Profile'),
    path('profile/<int:pk>/update/',views_profile.profile_update,name='Profile Update'),
    path('profile/<int:pk>/change_password/',views_auth.change_password,name='Change Password'),
    
    path('forget_password/',views_auth.forget_password,name='Forget Password'),
    path('reset_password_send/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/pwd_reset_send.html'),name='password_reset_send'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/pwd_reset_confirm.html'),name="password_reset_confirm"),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/pwd_reset_done.html'),name="password_reset_complete"),
    path('api/',include('cartapp.urls')),
]
