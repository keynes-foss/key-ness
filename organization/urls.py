from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'(?P<year>\d{4}-\d{4})/(?P<section>\w)/(?P<course>\w)/(?P<klass>\w)', 'organization.views.view_klass', name='klass'),
    url(r'(?P<year>\d{4}-\d{4})/(?P<section>\w)/(?P<course>\w)', 'organization.views.view_course', name='course'),

    url(r'(?P<year>\d{4}-\d{4})/(?P<section>\w)', 'organization.views.view_section', name='section'),
    url(r'(?P<year>\d{4}-\d{4})', 'organization.views.view_year', name='year'),


    #url(r'^ciappino/', include('ciappino.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
