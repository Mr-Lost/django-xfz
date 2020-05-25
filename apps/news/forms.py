from django import forms
from apps.forms import FormMixin


class PublishCommentForm(forms.Form, FormMixin):
    content = forms.CharField(max_length=None)
    news_id = forms.IntegerField()
