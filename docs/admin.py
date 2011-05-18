from django.contrib.admin import site
from docs.models import *

site.register(Document)
site.register(DocumentComment)
