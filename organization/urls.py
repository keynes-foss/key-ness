from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'(?P<year>\d{4}-\d{4})/project/(?P<project>\w+)', 'organization.views.view_project', name='project'),
    url(r'(?P<year>\d{4}-\d{4})/(?P<section>\w+)/(?P<course>\w+)/(?P<klass>\w+)', 'organization.views.view_klass', name='klass'),
    url(r'(?P<year>\d{4}-\d{4})/(?P<section>\w+)/(?P<course>\w+)', 'organization.views.view_course', name='course'),
    url(r'(?P<year>\d{4}-\d{4})/(?P<section>\w+)', 'organization.views.view_section', name='section'),
    url(r'(?P<year>\d{4}-\d{4})', 'organization.views.view_year', name='year'),


    url(r'subject/(?P<subject>\w*)', 'organization.views.view_subject', name='subject'),
    url(r'p/(?P<username>\w*)', 'organization.views.view_profile', name='profile'),

)
