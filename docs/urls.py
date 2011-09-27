from django.conf.urls.defaults import patterns, include, url



urlpatterns = patterns('',
	url(r'add/', 'docs.views.put_file', name='add_doc'),
	url(r'/(?P<file_id>\d)', 'docs.views.put_file', name='add_doc'),
	url(r'del/(?P<file_id>\d)', 'docs.views.del_file', name='del_doc'),
)
