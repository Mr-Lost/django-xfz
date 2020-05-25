from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegisterForm
from django.http import JsonResponse, HttpResponse
from utils import restful
from django.shortcuts import redirect, reverse
from utils.captcha.xfzcatpcha import Captcha
from io import BytesIO
from django.core.cache import cache


User = get_user_model()


@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, username=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)   # 使用django默认过期时间，即2星期
                else:
                    request.session.set_expiry(0)   # 浏览器关闭就过期
                return restful.ok()
            else:
                return restful.unauth(message='您的账号已经被冻结了！')
        else:
            return restful.params_error(message='手机号或者密码错误！')
    else:
        errors = form.get_errors()
        return restful.params_error(message=errors)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


@require_POST
def register(request):
    form = RegisterForm(request.POST)
    print('开始注册')
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone, username=username, password=password)
        login(request, user)
        print('登陆成功')
        return restful.ok()
    else:
        print('注册出错', form.get_errors())
        return restful.params_error(message=form.get_errors())


def img_captcha(request):
    text, image = Captcha.gene_code()
    out = BytesIO()   # BytesIO相当于一个管道，用来存储图片的流数据
    image.save(out, 'png')   # 将image对象保存到BytesIO中
    out.seek(0)   # 将BytesIO的文件指针移动到最开始位置，为了后面read
    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()   # 获取当前指针位置，即获取图片大小
    cache.set(text.lower(), text.lower(), 5*60)   # 验证码保存5分钟
    print('图形验证码是：', text.lower())
    return response


def sms_captcha(request):
    telephone = request.GET.get('telephone')
    code = Captcha.gene_text()
    # result = function_sendmsg(telephone, code)
    cache.set(telephone, code, 5*60)
    print('短信验证码是：', code)
    return restful.ok()


def cache_test(request):
    cache.set('username', 'limbor', 60)
    username = cache.get('username')
    print(username)
    return HttpResponse('success')
