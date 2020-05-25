from django import forms
from apps.forms import FormMixin
from apps.news.models import News, Banner
from apps.course.models import Course, CourseCategory, Teacher


class NewsCategoryEditForm(forms.Form, FormMixin):
    pk = forms.IntegerField(error_messages={'required': '必须传入一个pk值'})
    name = forms.CharField(max_length=100)


class NewsPublishForm(forms.ModelForm, FormMixin):
    category_id = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'pub_time', 'author']


class BannerForm(forms.ModelForm, FormMixin):

    class Meta:
        model = Banner
        fields = ('priority', 'link_to', 'image_url')


class EditBannerForm(forms.ModelForm, FormMixin):
    pk = forms.IntegerField()

    class Meta:
        model = Banner
        fields = ('priority', 'link_to', 'image_url')


class NewsEditForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()
    pk = forms.IntegerField()

    class Meta:
        model = News
        exclude = ('category', 'author', 'pub_time')


class CoursePublishForm(forms.ModelForm, FormMixin):
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()

    class Meta:
        model = Course
        exclude = ['category', 'pub_time', 'teacher']


class CourseCategoryAddForm(forms.ModelForm, FormMixin):
    pass

