from django import forms

from organization.models import OrganizationTag

class PostForm(forms.Form):
	title = forms.CharField()
	content= forms.CharField(widget=forms.Textarea)

	tags = forms.ModelMultipleChoiceField(queryset = OrganizationTag.objects.all())


class CommentForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea)
	