from django.http import *
from organization.models import *
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
import settings


try:
	import json
except:
	import simplejson as json

def view_year(request, year):
	y = Year.objects.get(name = year)
	res = {
		_("Schools"):[{
			"name":str(s),
			'url':s.url()
		} for s in y.sections.all()],
		_("Projects"):[{
			"name":str(s),
			'url':s.url()
		} for s in y.alloc_projects.all()]
	}
	psts =  Year.posts.related(y)
	return render_to_response('year.html', {
                'content':res,
                'breadcrumbs':[{
                        "name":y.name,
                        "url":str(y.url())
                }],
                'title':y.name,
                "message":_("School Info:"),
		'all_posts':psts ,
		'school_name':settings.SCHOOL_NAME,
	'user_loggedin':request.user.is_anonymous()==False,
	'selfurl':request.path
        })

def view_section(request, year, section):
	y = Year.objects.get(name = year)
	s = SchoolSection.objects.get(year = y, suffix = section)
	res = {_("Courses"):[{
		"name":str(c),
		'url':str(c.url())
	} for c in s.courses.all()]}
	psts =  Year.posts.related(s)
	return render_to_response('year.html', {
                'content':res,
                'breadcrumbs':[{
                        "name":y.name,
                        "url":str(y.url())
                },{
                        "name":s.name,
                        "url":str(s.url())
                }],
                'title':s.name,
                "message":_("Section info:"),
		'all_posts':psts  ,
		'school_name':settings.SCHOOL_NAME,
	'user_loggedin':request.user.is_anonymous()==False,
	'selfurl':request.path

        })

def view_course(request, year, section, course):
	y = Year.objects.get(name = year)
	s = SchoolSection.objects.get(year = y, suffix = section)
	c = Course.objects.get(section = s, name = course)
	res = {"Courses":[{ 
        "name":str(k), 
        'url':str(k.url()), 
        
    } for k in c.klasses.all()]}
	psts =  Year.posts.related(c)
        return render_to_response('year.html', {
                "content":res,
                'breadcrumbs':[{
                        "name":y.name,
                        "url":str(y.url())
                },{
                        "name":s.name,
                        "url":str(s.url())
                },{
                        "name":c.name,
                        "url":str(c.url())
                }],
                'title':c.name,
                "message":_("Course info:"),
		'all_posts':psts  ,
		'school_name':settings.SCHOOL_NAME,
	'user_loggedin':request.user.is_anonymous()==False,
	'selfurl':request.path

        })

def view_klass(request, year,section, course, klass):
	y = Year.objects.get(name = year)
	s = SchoolSection.objects.get(year = y, suffix = section)
	c = Course.objects.get(section = s, name = course)
	k = Klass.objects.get(course = c, name = klass)
	psts =  Year.posts.related(k)
	students = []
	teachers = []
	for q in k.students.all():
		students.append({
			"name":str(q.student.name()),
			'url':str(q.student.url()),
			} )
	for q in k.teachers.all():
		su = q.subject
		teachers.append({
			"name":str(q.teacher.name()),
			'url':str(q.teacher.url()),
			'subjects':[{"name":su.name, "color":su.color, "url":str(su.url())} ]
			} )


	psts =  Klass.posts.related(k)

	return render_to_response('class.html', {
		'breadcrumbs':[{
              	"name":y.name,
                     "url":str(y.url())
		},{
			"name":s.name,
			"url":str(s.url())
		},{
			"name":c.name,
			"url":str(c.url())
		},{
			"name":k.name,
			"url":str(k.url())
		}],
		'title':str(k),
		"message":_("Class info:"),
		"students":students,
		'teachers':teachers,
		'all_posts':psts  ,
		'school_name':settings.SCHOOL_NAME,
	'user_loggedin':request.user.is_anonymous()==False,
	'selfurl':request.path

        })

def view_subject(request, subject):
	c = Subject.objects.get(name=subject)
	t = TeacherProfile.objects.filter(subject=c)
	psts =  Subject.posts.related(c)
        return render_to_response('subject.html', {
                'breadcrumbs':[{
                        "name":c.name,
                        "url":str(c.url())
                }],
		'content':{
			'Teachers':[
			{'name':str(te),
			'url': te.url()} for te in t]
		},
                'title':c.name,
                "message":_("Subject:"),
		'all_posts':psts  ,
		'school_name':settings.SCHOOL_NAME,
	'user_loggedin':request.user.is_anonymous()==False,
	'selfurl':request.path

        })


def view_project(request, year,project):
	y = Year.objects.get(name = year)
	k = Project.objects.get(year = y, id = project)
	students = []
	teachers = []
	for q in k.students.all():
		students.append({
			"name":str(q.student.name()),
			#'url':str(q.student.url()),
			} )
	for q in k.teachers.all():
		su = q.subject
		teachers.append({
			"name":str(q.teacher.name()),
			#'url':str(q.teacher.url()),
			'subjects':[{"name":su.name, "color":su.color, "url":str(su.url())} ]
			} )
	psts =  Klass.posts.related(k)
	return render_to_response('class.html', {
		'breadcrumbs':[{
              	"name":y.name,
                     "url":str(y.url())
		},{
			"name":k.name,
			"url":str(k.url())
		}],
		'title':str(k),
		"message":_("Project info:"),
		"students":students,
		'teachers':teachers,
		'all_posts':psts  ,
		'school_name':settings.SCHOOL_NAME,
	'user_loggedin':request.user.is_anonymous()==False,
	'selfurl':request.path

        })

def view_profile(request, username):
	return render_to_response('profile.html', {})

def mainview(request):
	import datetime
	y = int(datetime.date.today().year)
	ypo = y+1
	url = Year.objects.filter(name__contains = str(y))[0].url()

	return HttpResponseRedirect(url)
