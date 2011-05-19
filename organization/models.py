from django.db import models
from django.contrib.auth.models import User



class Year(models.Model):
	name = models.TextField(unique=True)
	def __unicode__(self):
		return self.name
	@models.permalink
	def url(self):
		return ('year', (), {'year':self.name})# Create your models here.

class SchoolSection(models.Model):
	name = models.TextField()
	suffix = models.TextField()	
	description = models.TextField(blank = True, null=True)
	year = models.ForeignKey(Year, related_name = "sections")
	def __unicode__(self):
		return self.name + " (%s)" % self.suffix
	class Meta:
		unique_together = ("name", "year")
	@models.permalink
	def url(self):
		return ('section', (), {'year':self.year.name, "section":self.suffix})


class Project(models.Model):
	name = models.TextField()
	year = models.ForeignKey(Year, related_name = "alloc_projects")
	def __unicode__(self):
		return self.name 
	@models.permalink
	def url(self):
		return ('project', (), {'year':self.year.name, "project":str(self.id)})


class Course(models.Model):
	name = models.TextField()
	section = models.ForeignKey(SchoolSection, related_name ="courses")
	description = models.TextField(blank = True, null=True)
	@models.permalink
	def url(self):
		return ('course', (), {'year':self.section.year.name, 'section':self.section.suffix, 'course':self.name})# Create your models here.

	def __unicode__(self):
		return self.name + self.section.suffix
	
class Klass(models.Model):
	name = models.TextField()
	course = models.ForeignKey(Course, related_name = "klasses")
	@models.permalink
	def url(self):
		return ('klass', (), {'year':self.course.section.year.name, 'section':self.course.section.suffix, 'course':self.course.name, 'klass':self.name})# Create your models here.
	
	class Meta:
		unique_together = ('name', 'course', )
	def __unicode__(self):
		return self.name+str(self.course)

class StudentProfile(models.Model):
	user = models.ForeignKey(User, related_name="student_profile", unique=True)
	def __unicode__(self):
		return self.user.username

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
	def __unicode__(self):
		return self.name
	@models.permalink
	def url(self):
		return ('subject', (), {'subject':self.name})# Create your models here.

class TeacherProfile(models.Model):
	user = models.ForeignKey(User, related_name="teacher_profile", unique=True)
	subject = models.ManyToManyField(Subject)
	def __unicode__(self):
		return self.user.username + " (%s)" % ",".join([str(a) for a in self.subject.all()])
	@models.permalink
	def url(self):
		return ('profile', (), {'username':self.user.username})
	def name(self):
		return self.user.get_full_name() or self.user.username

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





























