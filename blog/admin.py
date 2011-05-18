from django.contrib.admin import site
from blog.models import *

site.register(Blog)
site.register(Post)
site.register(Comment)
