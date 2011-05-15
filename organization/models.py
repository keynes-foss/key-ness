from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Year(models.Model):
	name = models.TextField()

class Course(models.Model):
	name = models.TextField()
	description = models.TextField()
	
class Klass(models.Model):
	name = model.TextField()
	course = models.ForeignKey(Course)
	class Meta:
		unique_together = ('name','course',)

class StudentProfile(models.Model):
	user = models.ForeignKey(User)
	
class StudentKlass(models.Model):
	student = models.ForeignKey(StudentProfile)
	klass = models.ForeignKey(Klass)	
	year = models.ForeignKey(Year)

class Subject(models.Model):
	name = models.TextField()

class TeacherProfile(models.Model):
	user = models.ForeignKey(User)
	subject = models.ManyToManyField(Subject)
	
class TeacherKlass(models.Model):
	teacher = models.ForeignKey(TeacherProfile)
	klass = models.ForeignKey(Klass)
        year = models.ForeignKey(Year)
	subject = models.ForeignKey(Subject)







