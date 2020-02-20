from django.conf.urls import url
from django.conf.urls.static import static

from photoproject import settings
from . import views

urlpatterns = [

    url(r'(?P<id>\d+)/post_delete/$', views.post_delete, name="post_delete"),
    url(r'(?P<id>\d+)/post_edit/$', views.post_edit, name="post_edit"),
    url(r'(?P<id>\d+)/(?P<slug>[\w-]+)/$', views.post_detail, name="post_detail"),
    # url(r'post_create/$', views.post_create, name="post_create"),
    # url(r'(?P<id>\d+)/post_edit/$', views.post_edit, name="post_edit"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

