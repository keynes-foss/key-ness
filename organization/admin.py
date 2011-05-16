from django.contrib.admin import site
from organization.models import *

site.register(Year)
site.register(SchoolSection)
site.register(Project)
site.register(Course)
site.register(Klass)
site.register(StudentProfile)
site.register(StudentProject)
site.register(StudentKlass)
site.register(KlassProject)
site.register(Subject)
site.register(TeacherProfile)
site.register(TeacherKlass)
site.register(TeacherProject)