from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('deleted/', views.deleted_posts, name='deleted_posts'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/edit/', views.post_update, name='post_update'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('<int:pk>/restore/', views.post_restore, name='post_restore'),
    path('<int:pk>/hard-delete/', views.post_hard_delete, name='post_hard_delete'),

]