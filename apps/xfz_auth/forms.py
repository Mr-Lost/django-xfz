from django import forms
from apps.forms import FormMixin
from django.core.cache import cache
from .models import User


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=20, min_length=6, error_messages={'max_length': '密码最多不超过20个字符！',
                                                                            'min_length': '密码最少不少于6个字符！'})
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=20, min_length=6, error_messages={'max_length': '密码最多不超过20个字符！',
                                                                             'min_length': '密码最少不少于6个字符！'})
    password2 = forms.CharField(max_length=20, min_length=6, error_messages={'max_length': '密码最多不超过20个字符！',
                                                                             'min_length': '密码最少不少于6个字符！'})
    img_captcha = forms.CharField(min_length=4, max_length=4)
    sms_captcha = forms.CharField(min_length=4, max_length=4)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        telephone = cleaned_data.get('telephone')
        if not telephone:
            raise forms.ValidationError('请输入手机号码！')
        if len(telephone) != 11:
            raise forms.ValidationError('手机号码无效！')

        username = cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('请输入用户名！')

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if not password1:
            raise forms.ValidationError('请输入密码！')
        if not password2:
            raise forms.ValidationError('请再次输入密码！')
        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致！')

        img_captcha = cleaned_data.get('img_captcha')
        if not img_captcha:
            raise forms.ValidationError('请输入图形验证码！')

        cached_img_captcha = cache.get(img_captcha.lower())
        if not cached_img_captcha or cached_img_captcha.lower() != img_captcha.lower():
            raise forms.ValidationError('图形验证码错误！')

        sms_captcha = cleaned_data.get('sms_captcha')
        if not sms_captcha:
            raise forms.ValidationError('请输入短信验证码！')

        cached_sms_captcha = cache.get(telephone)
        if not cached_sms_captcha or cached_sms_captcha.lower() != sms_captcha.lower():
            raise forms.ValidationError('短信验证码错误！')

        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError('该手机号已经被注册！')

        exists_username = User.objects.filter(username=username).exists()
        if exists_username:
            raise forms.ValidationError('该用户名已被注册！')
