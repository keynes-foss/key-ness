from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
url(r'^$', 'organization.views.mainview'),
url(r'^org/', include('organization.urls')),
url(r'^posts/', include('blog.urls')),
#url(r'^docs/', include('docs.urls')),
url(r'^admin/', include(admin.site.urls)),
url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
url(r'^logout/', 'django.contrib.auth.views.logout'),
)
