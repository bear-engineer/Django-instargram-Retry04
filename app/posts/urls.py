from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    # defort 는 post-list page
    path('', views.post_list, name='post-list'),
    # post-create
    path('postcreate/', views.post_create, name='post-create'),
    path('<int:pk>/postdelete/', views.post_delete, name='post-delete'),
    path('<post_pk>/comment/', views.comment, name='comment'),
]