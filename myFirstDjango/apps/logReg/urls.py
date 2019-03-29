from django.conf.urls import url
from . import views
# This is where the actual routes are made with their methods.
                    
urlpatterns = [
    # localhost:8000/
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^enter$', views.enterSite),
    url(r'^wall$', views.wall),
    url(r'^create/post$', views.createPost),
    url(r'^exit$', views.exitSite),
    url(r'^delete/post/(?P<post_id>[0-9]+)$', views.deletePost),
    url(r'^edit/post/(?P<post_id>[0-9]+)$', views.editPost),
    url(r'^update/post/(?P<post_id>[0-9]+)$', views.updatePost),
]