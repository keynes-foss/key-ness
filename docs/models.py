from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
        uploader = models.ForeignKey(User)
        description = models.TextField()
        content = models.TextField()
        mime_type = models.TextField()
        private = models.BooleanField(default = True)
        protected = models.BooleanField(default = True)
        uploaded_at = models.DateTimeField(auto_now = True, editable = False)
        last_modified = models.DateTimeField(auto_now_save = True, editable = False)

class DocumentComment(models.Model):
        document = models.ForeignKey(Document)
        author = models.ForeignKey(User)
        content = models.TextField()
        date = models.DateTimeField()