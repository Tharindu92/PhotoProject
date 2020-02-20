from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from photo import views
from photo.views import CreatePostView
from photoproject import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.post_list, name="post_list"),
    #url(r'^photo/post_create/$', views.post_create, name="post_create"),
    url(r'^photo/', include(('photo.urls', 'photo'), namespace="photo")),
    url(r'^login/$', views.user_login, name="user_login"),
    url(r'^logout/$', views.user_logout, name="user_logout"),
    url(r'^photo/post_create/$', CreatePostView.as_view(), name='post_create'),
    # url(r'^$', PostListView.as_view(), name='post_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)