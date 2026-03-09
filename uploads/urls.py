from django.urls import path
from . import views

app_name = 'uploads'

urlpatterns = [
    path('', views.file_list, name='upload_list'),
    path('upload/', views.upload_file, name='upload_file'),
    path('delete/<int:pk>/', views.delete_file, name='delete_file'),
    path('hard-delete/<int:pk>/', views.hard_delete_file, name='hard_delete_file'),
    path('restore/<int:pk>/', views.restore_file, name='restore_file'),
]