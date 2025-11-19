from django.contrib import admin
from django.urls import path, include
from . import views as core_views
from accounts import views as accounts_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
    path('about/', core_views.about, name='about'),
    path('comments/', include('comments.urls', namespace='comments')),
    path('', accounts_views.login_view, name="home"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
