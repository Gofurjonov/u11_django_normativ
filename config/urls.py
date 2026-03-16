from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings
from django.shortcuts import redirect


def home_redirect(request):
    return redirect('post_list')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),
    path('books/', include('books.urls')),
    path('posts/', include('posts.urls')),
    path('accounts/', include('accounts.urls')),
    path('notifications/', include('notifications.urls')),
    path('uploads/', include('uploads.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
