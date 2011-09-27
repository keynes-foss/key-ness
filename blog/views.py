from blog.forms import *
from organization.models import *
from django.shortcuts import render_to_response
from django.http import *
import settings
from django.template import Context, Template, RequestContext

def get_post(request, id):
	return render_to_response('post.html', {'school_name':settings.SCHOOL_NAME,
	'user_loggedin':request.user.is_anonymous()==False,
	'all_posts':[{'title':post.title,
			'author':post.author.username,
			'content':post.content,
			'url':post.url(),
			'tags':[{
					'name':tag.name,
					'url':tag.refers_to,
					'type':tag.type} for tag in post.related_to.all()]
				
			
				} for post in Post.objects.filter(id=id)]})

def add_post(request):
	if request.method == 'POST': 
		form = PostForm(request.POST) 
		if form.is_valid(): 
			p = Post()
			p.author = request.user
			p.content = form.cleaned_data['content']
			p.title = form.cleaned_data['title']
			p.save()
			for t in form.cleaned_data['tags']:
				p.related_to.add(t)
			#p.related_to.add(OrganizationTag.objects.filter(refers_to=request.path)[0])
			
			return HttpResponseRedirect('/') 
	else:
		form = PostForm()
		item = request.REQUEST.get('related_to', None)
		
	
	return render_to_response('form.html', {
		'form': form,
		'school_name':settings.SCHOOL_NAME,
	'user_loggedin':request.user.is_anonymous()==False

	}, context_instance=RequestContext(request))

def edit_post(request, id):
	p = Post.objects.get(id=id)
	if request.method == 'POST': # If the form has been submitted...
		form = PostForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			# Process the data in form.cleaned_data
			# ...
			return HttpResponseRedirect('/thanks/') # Redirect after POST	
	else:
		form = PostForm()
		# An unbound form
		form.author = None

	return render_to_response('form.html', {
		'form': form,
		'school_name':settings.SCHOOL_NAME,
	'user_loggedin':request.user.is_anonymous()==False

	})


def del_post(request, id):
	Post.objects.get(id=id).delete()

def add_comment(request):
	if request.method == 'POST': # If the form has been submitted...
		form = PostForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			# Process the data in form.cleaned_data
			# ...
			return HttpResponseRedirect('/thanks/') # Redirect after POST	
	else:
		form = PostForm()
		# An unbound form
		form.author = None

	return render_to_response('form.html', {
		'form': form,
		'school_name':settings.SCHOOL_NAME,
	'user_loggedin':request.user.is_anonymous()==False

	})

def edit_comment(request, id):
	if request.method == 'POST': # If the form has been submitted...
		form = PostForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			# Process the data in form.cleaned_data
			# ...
			return HttpResponseRedirect('/thanks/') # Redirect after POST	
	else:
		form = PostForm()
		# An unbound form
		form.author = None

	return render_to_response('form.html', {
		'form': form,
		'school_name':settings.SCHOOL_NAME,
	'user_loggedin':request.user.is_anonymous()==False

	})

def del_comment(request, id):
	Comment.objects.get(id=id).delete()