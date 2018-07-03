from django.urls import path
from . import views

app_name = 'members'
urlpatterns = [
    path('signin',views.sign_in, name='sign-in'),
    path('signup/',views.sign_up, name='sign-up'),
    path('signout/', views.sign_out, name='sign-out'),
    path('facebook-login/', views.facebook_login, name='sig-in-facebook'),
]