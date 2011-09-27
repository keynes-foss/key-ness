from django.db import models

class Block(models.Model):
	title = models.TextField()
	
	def render_content(self, *args, **kwargs):
		return ""

	def render(self):
		return {
			"title":self.title,
			"content": self.render_content()
		}

	class Meta:
		abstract = True

class LinksBlockLink(models.Model):
	url = models.UrlField()
	title = models.TextField()
	text = models.TextField()

class LinksBlock(Block):
	links = models.ManyToManyField(LinksBlockLink)
	
	def render_content(self):
		return [{"url": a.url, "title": a.title, "text": a.text, "type":"link"} for a in links.all()]

class Headline(models.Model):
	text = models.TextField()
	valid = models.BooleanField()

	