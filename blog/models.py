from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from organization.models import OrganizationTag




class Blog(models.Model):
	owner = models.ForeignKey(User)
	title = models.TextField()
	static_content = models.TextField()

	def __unicode__(self):
		return self.title

	@models.permalink
	def url(self):
		return ('get_blog', (), {
			'year': self.created.year,
			'month': self.created.month,
			'day': self.created.day
			})


class Post(models.Model):
	author = models.ForeignKey(User)
	content = models.TextField()
	title = models.TextField()
	related_to = models.ManyToManyField(OrganizationTag)
	date = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.title
	@models.permalink
	def url(self):
		return ('get_post', (), {
			'id': self.id})
class Comment(Post):
	for_post = models.ForeignKey(Post, related_name="comments")


