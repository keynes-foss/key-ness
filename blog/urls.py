from django.conf.urls.defaults import patterns, include, url



urlpatterns = patterns('',
	url(r'(?P<id>\d)', 'blog.views.get_post', name='get_post'),

	url(r'add/', 'blog.views.add_post', name='add_post'),
	url(r'edit/(?P<id>\d)', 'blog.views.edit_post', name='edit_post'),	
	url(r'del/(?P<id>\d)', 'blog.views.del_post', name='del_post'),
	
	url(r'addcomment/', 'blog.views.add_comment', name='add_comment'),
	url(r'editcomment/(?P<id>\d)', 'blog.views.edit_comment', name='edit_comment'),
	url(r'delcomment/(?P<id>\d)', 'blog.views.del_comment', name='del_comment'),	
)
