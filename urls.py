from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import *
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from finisht.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    ('^tools/$', direct_to_template, {'template': 'tools.html'}),
    ('^404/$', direct_to_template, {'template': '404.html'}),
    ('^500/$', direct_to_template, {'template': '500.html'}),
    ('^login/$', login, {'template_name': 'login.html'}),
    (r'^friends/approve/(\d+)$', approve_friend),
    (r'^friends/delete/(\d+)$', delete_friend),
    ('^logout/$', logout, {'next_page': '/'}),
    ('^toggle_friends/$', toggle_friends),
    (r'^delete/(\d+)$', delete_success),
    ('^friends/$', friends),
    ('^signup/$', signup),
    ('^$', home),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT.replace('\\','/')}),
    
)
