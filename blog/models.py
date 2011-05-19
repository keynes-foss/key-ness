from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
        owner = models.ForeignKey(User)
        title = models.TextField()
        static_content = models.TextField()

        def __unicode__(self):
                return self.title

class Post(models.Model):
        author = models.ForeignKey(User)
        content = models.TextField()
        title = models.TextField()
        related_to = models.ManyToManyField(OrganizationTag)

        def __unicode__(self):
                return self.title
        
class Comment(Post):
        refers_to = models.ForeignKey(Post)

class OrganizationTag(models.Model):
        name = models.TextField()
        refers_to=models.TextField()
        
        def __unicode__(self):
                return self.name
        def url(self):
                return se