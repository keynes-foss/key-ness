from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

import settings


class OrganizationTag(models.Model):
        name = models.TextField()
        type = models.TextField()
        refers_to=models.TextField()
        
        def __unicode__(self):
                return self.name
        def url(self):
                return self.refers_to

from blog.models import Post
from blog.models import Comment

def url_for(user):
	if TeacherProfile.objects.filter(user=user).count()==1:
		return TeacherProfile.objects.get(user=user).url()
	return StudentProfile.objects.get(user=user).url()

def related_urls(item): 
	urls = []
	if type(item) is Year:
		print "year"
		urls.append(item.url())
		for section in item.sections.all():
			urls.append(section.url())
			for course in section.courses.all():
				urls.append(course.url())
				for klass in course.klasses.all():
					urls.append(klass.url())
		for project in item.alloc_projects.all():
			urls.append(project.url())

	elif type(item) is SchoolSection:
		urls.append(item.url())
		for course in item.courses.all():
				urls.append(course.url())
				for klass in course.klasses.all():
					urls.append(klass.url())
	elif type(item) is Project:				
		urls.append(item.url())
	elif type(item) is Course:		
		urls.append(item.url())
		for klass in item.klasses.all():
			urls.append(klass.url())
	elif type(item) is Klass:		
		urls.append(item.url())
	elif type(item) is Subject:		
		urls.append(item.url())

	elif type(item) in [TeacherProfile, StudentProfile]:		
		urls.append(item.url())
	return urls


class PostManager(models.Manager):
	def related(self, item, user, is_user=False):
		urls = related_urls(item)
		from django.db.models import Q
		t = OrganizationTag.objects.filter(refers_to__in = urls)
		if not is_user:
			p = Post.objects.filter(related_to__in = t).distinct().order_by('-date')
		else:	
			p = Post.objects.filter(Q(related_to__in = t) | Q(author = item.user)).distinct().order_by('-date')

		posts = []
		for post in p:
			a = {}
			a['id'] = post.id
			a['title'] = post.title
			a['author'] = {
				'name':post.author.username,
				'url':url_for(post.author)
			}
			a['owner'] = user == post.author
			a['content'] = post.content
			a['url'] = post.url()
			a['tags'] = []
			for tag in post.related_to.all():
				a['tags'].append({
					'name':tag.name,
					'url':tag.refers_to,
					'type':tag.type
				})
				if tag.type=="subject":
					a['type'] = tag.name
			
			posts.append(a)
		
		styles = {}
		for post in posts:
			for tag in post['tags']:
				if tag['type'] == "subject":
					styles[tag['name']]="#%s" % Subject.objects.get(name=tag['name']).color
				
		return posts, styles


class DocsManager(models.Manager):
	def related(self, item, user, is_user=False):
		urls = related_urls(item)
		from django.db.models import Q
		t = OrganizationTag.objects.filter(refers_to__in = urls)
		if not is_user:
			p = Document.objects.filter(tags__in = t).distinct().order_by('-uploaded_at')
		else:	
			p = Document.objects.filter(Q(tags__in = t) | Q(author = item.user)).distinct().order_by('-uploaded_at')
		docs = []

		for doc in p :
			if ((doc.uploader==user) or not doc.private):
				a = {}
				a['owner'] = user == doc.uploader 
				a['name'] = doc.filename
				a['filetype'] = doc.mime_type
				a['url'] = doc.url()
				docs.append(a)




class Year(models.Model):
	name = models.TextField(unique=True)
	posts = PostManager()
	objects = models.Manager()
	def __unicode__(self):
		return self.name
	def representation(self):
		return self.name
	@models.permalink
	def url(self):
		return ('year', (), {'year':self.name})# Create your models here.

class SchoolSection(models.Model):
	name = models.TextField()
	suffix = models.TextField()	
	description = models.TextField(blank = True, null=True)
	year = models.ForeignKey(Year, related_name = "sections")
	posts = PostManager()
	objects = models.Manager()
	def __unicode__(self):
		return self.name + " (%s)" % self.suffix
	def representation(self):
		return self.name 
	class Meta:
		unique_together = ("name", "year")
	@models.permalink
	def url(self):
		return ('section', (), {'year':self.year.name, "section":self.suffix})


class Project(models.Model):
	name = models.TextField()
	year = models.ForeignKey(Year, related_name = "alloc_projects")
	posts = PostManager()
	objects = models.Manager()
	def __unicode__(self):
		return self.name 
	def representation(self):
		return self.name
	@models.permalink
	def url(self):
		return ('project', (), {'year':self.year.name, "project":str(self.id)})


class Course(models.Model):
	name = models.TextField()
	section = models.ForeignKey(SchoolSection, related_name ="courses")
	description = models.TextField(blank = True, null=True)
	posts = PostManager()
	objects = models.Manager()
	@models.permalink
	def url(self):
		return ('course', (), {'year':self.section.year.name, 'section':self.section.suffix, 'course':self.name})# Create your models here.
	def representation(self):
		return self.name + self.section.suffix
	def __unicode__(self):
		return self.name + self.section.suffix
	
class Klass(models.Model):
	name = models.TextField()
	course = models.ForeignKey(Course, related_name = "klasses")
	posts = PostManager()
	objects = models.Manager()
	@models.permalink
	def url(self):
		return ('klass', (), {'year':self.course.section.year.name, 'section':self.course.section.suffix, 'course':self.course.name, 'klass':self.name})# Create your models here.
	def representation(self):
		return self.name+str(self.course)
	class Meta:
		unique_together = ('name', 'course', )
	def __unicode__(self):
		return self.name+str(self.course)

class Profile(models.Model):
	user = models.ForeignKey(User, unique=True)

	def __unicode__(self):
		return self.user.username
	def representation(self):
		return self.user.get_full_name()or self.user.username

	def name(self):
		return self.user.get_full_name() or self.user.username
	@models.permalink
	def url(self):
		return ('profile', (), {'username':self.user.username})
	
	class Meta:
		abstract=True


class StudentProfile(Profile):
	posts = PostManager()
	objects = models.Manager()
	def __unicode__(self):
		return self.user.username
	def representation(self):
		return self.user.get_full_name()
	def name(self):
		return self.user.get_full_name() or self.user.username
	@models.permalink
	def url(self):
		return ('profile', (), {'username':self.user.username})


###########################################################################################################
# M2M Reification
###########################################################################################################
	

class StudentKlass(models.Model):
	klass  = models.ForeignKey(Klass, related_name ="students")	
	student = models.ForeignKey(StudentProfile)
	year = models.ForeignKey(Year)
	def __unicode__(self):
		return "%s - %s in %s" % (str(self.student),str(self.klass), str(self.year), ) 


class StudentProject(models.Model):
	project = models.ForeignKey(Project, related_name = "students")	
	student = models.ForeignKey(StudentProfile)
	year = models.ForeignKey(Year)
	def __unicode__(self):
		return "%s - %s in %s" % (str(self.student),str(self.project ), str(self.year), ) 
	

class KlassProject(models.Model):
	klass = models.ForeignKey(Klass, related_name = "projects")	
	year = models.ForeignKey(Year, related_name = "projects")
	project = models.ForeignKey(Project, related_name="klasses")
	def __unicode__(self):
		return "%s - %s in %s" % (str(self.klass),str(self.project), str(self.year), ) 


class Subject(models.Model):
	name = models.TextField()
	color = models.TextField(default = "ffffff")
	posts = PostManager()
	objects = models.Manager()
	def __unicode__(self):
		return self.name
	def representation(self):
		return self.name
	@models.permalink
	def url(self):
		return ('subject', (), {'subject':self.name})# Create your models here.

class TeacherProfile(Profile):
	subject = models.ManyToManyField(Subject)
	posts = PostManager()
	objects = models.Manager()

###########################################################################################################
# M2M Reification
###########################################################################################################

class TeacherKlass(models.Model):
	
	klass = models.ForeignKey(Klass, related_name ="teachers")
	teacher = models.ForeignKey(TeacherProfile)
	year = models.ForeignKey(Year)
	subject = models.ForeignKey(Subject)
	def __unicode__(self):
		return "%s - %s in %s teaching %s" % (str(self.teacher),str(self.klass), str(self.year), str(self.subject), ) 

	@models.permalink
	def url(self):
		return ('year', (), {'year':self.name})# Create your models here.


class TeacherProject(models.Model):

	project = models.ForeignKey(Project, related_name ="teachers")
	teacher = models.ForeignKey(TeacherProfile)
	year = models.ForeignKey(Year)
	subject = models.ForeignKey(Subject)
	def __unicode__(self):
		return "%s - %s in %s teaching %s" % (str(self.teacher),str(self.project), str(self.year), str(self.subject), ) 
	@models.permalink
	def url(self):
		return ('year', (), {'year':self.name})# Create your models here.



def create_org_tag_by_instance(sender, **kwargs):
	t = OrganizationTag()
	i = kwargs['instance']
	n_n = i.representation()
	n_r = i.url()
	n_t = i._meta.module_name
	t.name = n_n
	t.refers_to = n_r
	t.type = n_t
	t.save()


post_save.connect(create_org_tag_by_instance, sender=Year, weak=False)
post_save.connect(create_org_tag_by_instance, sender=TeacherProfile, weak=False)
post_save.connect(create_org_tag_by_instance, sender=Subject, weak=False)
post_save.connect(create_org_tag_by_instance, sender=StudentProfile, weak=False)
post_save.connect(create_org_tag_by_instance, sender=SchoolSection, weak=False)
post_save.connect(create_org_tag_by_instance, sender=Course, weak=False)
post_save.connect(create_org_tag_by_instance, sender=Klass, weak=False)
post_save.connect(create_org_tag_by_instance, sender=Project, weak=False)



























