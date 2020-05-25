from utils import restful
from django.shortcuts import redirect


def xfz_login_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='请先登录！')
            else:
                return redirect('/')
    return wrapper
