from django.http import HttpResponse
from organization.models import *
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
try:
	import json
except:
	import simplejson as json

def view_year(request, year):
	y = Year.objects.get(name = year)
	res = [{
		"name":str(s),
		'url':str(s.url())
	} for s in y.sections.all()]
	return render_to_response('year.html', {
                'content':res,
                'breadcrumbs':[{
                        "name":y.name,
                        "url":str(y.url())
                }],
                'title':y.name,
                "message":_("School sections available:")
        })

def view_section(request, year, section):
	y = Year.objects.get(name = year)
	s = SchoolSection.objects.get(year = y, suffix = section)
	res = [{
		"name":str(c),
		'url':str(c.url())
	} for c in s.courses.all()]
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
                "message":_("Courses available in school Section:")
        })

def view_course(request, year, section, course):
	y = Year.objects.get(name = year)
	s = SchoolSection.objects.get(year = y, suffix = section)
	c = Course.objects.get(section = s, name = course)
	res = [{ 
        "name":str(k), 
        'url':str(k.url()), 
        
    } for k in c.klasses.all()]
        return render_to_response('course.html', {
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
                "message":_("Course info available:")
        })

def view_klass(request, year,section, course, klass):
	y = Year.objects.get(name = year)
	s = SchoolSection.objects.get(year = y, suffix = section)
	c = Course.objects.get(section = s, name = course)
	k = Klass.objects.get(course = c, name = klass)
	res = []
	for q in k.students.all():
		res.append({
			'type':"student",
			"name":str(q),
			#'url':str(q.url()),
			} )
	for q in k.teachers.all():
		res.append({
			'type':"teacher",
			"name":str(q),
			#'url':str(q.url()),
			} )

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
                'title':k.name,
                "message":_("Class info available:")
        })
