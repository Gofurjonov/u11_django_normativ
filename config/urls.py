from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings
from django.conf.urls.i18n import i18n_patterns


# from django.shortcuts import redirect


def home_redirect(request):
    from django.shortcuts import redirect
    return redirect('post_list')


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Til almashtirish
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),
    path('books/', include('books.urls')),
    path('posts/', include('posts.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('notifications/', include('notifications.urls')),
    path('uploads/', include('uploads.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
