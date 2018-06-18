
from django.conf.urls import url
from . import views

app_name = 'blog'


urlpatterns = [

    url(r'^$', views.post_list_view, name='post_list_view'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', views.post_detail_view,name='post_detail_view'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^newpost$', views.new_post, name='new_post'),
    url(r'^editpost/(?P<pk>\d+)/$', views.edit_post, name='edit_post'),
    url(r'^removepost/(?P<pk>\d+)/$', views.post_remove, name='post_remove'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]



