from django.http import *
from organization.models import *
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
import settings
from util import new_url

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
	psts, styles =  Year.posts.related(y,request.user)
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
	'selfurl':request.path,
	'styles':styles 
        })

def view_section(request, year, section):
	y = Year.objects.get(name = year)
	s = SchoolSection.objects.get(year = y, suffix = section)
	res = {_("Courses"):[{
		"name":str(c),
		'url':str(c.url())
	} for c in s.courses.all()]}
	psts, styles =  Year.posts.related(s,request.user)
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
	'selfurl':request.path,
	'styles':styles 

        })

def view_course(request, year, section, course):
	y = Year.objects.get(name = year)
	s = SchoolSection.objects.get(year = y, suffix = section)
	c = Course.objects.get(section = s, name = course)
	res = {"Courses":[{ 
        "name":str(k), 
        'url':str(k.url()), 
        
    } for k in c.klasses.all()]}
	psts, styles =  Year.posts.related(c,request.user)
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
	'selfurl':request.path,
	'styles':styles 

        })

def view_klass(request, year,section, course, klass):
	y = Year.objects.get(name = year)
	s = SchoolSection.objects.get(year = y, suffix = section)
	c = Course.objects.get(section = s, name = course)
	k = Klass.objects.get(course = c, name = klass)
	psts, styles =  Year.posts.related(k,request.user)
	students = []
	teachers = []
	for q in StudentProfile.objects.filter(studentklass__klass=k).distinct():
		students.append({
			"name":str(q.name()),
			'url':str(q.url()),
			} )
	for q in TeacherProfile.objects.filter(teacherklass__klass=k).distinct():
		teachers.append({
			"name":str(q.name()),
			'url':str(q.url()),
			'subjects':[{"name":su.name, "color":su.color, "url":str(su.url())} for su in Subject.objects.filter(teacherklass__teacher = q)]
			} )


	psts, styles =  Klass.posts.related(k,request.user)

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
	'selfurl':request.path,
	'styles':styles 

        })

def view_subject(request, subject):
	c = Subject.objects.get(name=subject)
	t = TeacherProfile.objects.filter(subject=c)
	psts, styles =  Subject.posts.related(c,request.user)
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
	psts, styles =  Klass.posts.related(k,request.user)
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
	'selfurl':request.path,
	'styles':styles 

        })

def view_profile(request, username):
	u = User.objects.get(username = username)
	import datetime
	y = int(datetime.date.today().year)
	y = Year.objects.filter(name__contains = str(y))[0]
	if u == request.user:
		#show private data 
		pass
	psts= []
	nt = TeacherProfile.objects.filter(user=u).count()
	ns = StudentProfile.objects.filter(user=u).count()

	if nt==1:
		tps = TeacherProfile.objects.get(user = u)
	if ns==1:	
		sps = StudentProfile.objects.get(user = u)

	psts,styles = Klass.posts.related(tps,request.user,True)		

	

	return render_to_response('profile.html', {'content':{
		"Classes":[
			{'name':tk, "url":tk.url()}
			for tk in Klass.objects.filter(teachers=TeacherKlass.objects.filter(year = y, teacher = tps))],
		"Projects":[
			{'name':tk, "url":tk.url()}
			for tk in Project.objects.filter(teachers=TeacherProject.objects.filter(year = y, teacher = tps))],
		"Subjects":[
			{'name':sub, "url":sub.url()}
			for sub in tps.subject.all()]
	},'all_posts':psts  , 
		'school_name':settings.SCHOOL_NAME,
	'user_loggedin':request.user.is_anonymous()==False,
	'selfurl':request.path,
	'styles':styles,
	'profile_teacher':nt==1,
	'profile_student':ns==1,
	'name': u.get_full_name(),
'breadcrumbs':[{
              	"name":y.name,
                     "url":str(y.url())
		}]


})





def mainview(request):
	import datetime
	y = int(datetime.date.today().year)
	ypo = y+1
	url = Year.objects.filter(name__contains = str(y))[0].url()

	return HttpResponseRedirect(url)
