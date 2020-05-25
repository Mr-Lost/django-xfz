from django.shortcuts import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt   # 用来表示一个视图可以被跨域访问
from django.views.decorators.http import require_http_methods
import string
import time
import random
import hashlib
import os
from django.http.response import JsonResponse, FileResponse
from django.conf import settings
import base64


# 用来判断是否要将文件上传到自己的服务器
try:
    UEDITOR_UPLOAD_TO_SERVER = settings.UEDITOR_UPLOAD_TO_SERVER
    if UEDITOR_UPLOAD_TO_SERVER:
        UEDITOR_UPLOAD_PATH = settings.UEDITOR_UPLOAD_PATH
        if not os.path.exists(UEDITOR_UPLOAD_PATH):
            os.mkdir(UEDITOR_UPLOAD_PATH)
except:
    pass


@method_decorator([csrf_exempt, require_http_methods(['GET', 'POST'])], name='dispatch')
class UploadView(View):
    def __init__(self):
        super(UploadView, self).__init__()

    def _random_filename(self, rawfilename):
        """
        生成为随机文件名，保证文件名不冲突
        :param rawfilename:
        :return:
        """
        letters = string.ascii_letters
        random_filename = str(time.time()) + ''.join(random.sample(letters, 5))
        filename = hashlib.md5(random_filename.encode('utf-8')).hexdigest()
        subffix = os.path.splitext(rawfilename)[-1]
        return filename + subffix

    def _json_result(self, state='', url='', title='', original=''):
        """
        返回指定格式的json数据
        :param state:
        :param url:
        :param title:
        :param original:
        :return:
        """
        result = {
            'state': state,
            'url': url,
            'title': title,
            'original': original
        }
        return JsonResponse(result)

    def _upload_to_server(self, upfile, filename):
        """
        上传到自己的服务器
        :param upfile:
        :param filename:
        :return:
        """
        with open(os.path.join(UEDITOR_UPLOAD_PATH, filename), 'wb') as fp:
            for chunk in upfile.chunks():
                fp.write(chunk)
        url = reverse('ueditor:send_file', kwargs={'filename': filename})
        return 'SUCCESS', url, filename, filename

    def _action_upload(self, request):
        """
        处理文件（图片，视频，普通文件）的上传
        :param request:
        :return:
        """
        upfile = request.FILES.get('upfile')
        filename = self._random_filename(upfile.name)

        if UEDITOR_UPLOAD_TO_SERVER:
            server_result = self._upload_to_server(upfile, filename)

        if server_result and server_result[0] == 'SUCCESS':
            return self._json_result(*server_result)
        else:
            return self._json_result()

    def _action_scrawl(self, request):
        base64data = request.form.get('upfile')
        img = base64.b64decode(base64data)   # 可逆的编码方式，用来加密非关键信息
        filename = self._random_filename('xx.png')
        with open(os.path.join(UEDITOR_UPLOAD_PATH, filename), 'wb') as fp:
            fp.write(img)
        url = reverse('ueditor:send_file', kwargs={'filename': filename})
        return self._json_result('SUCCESS', 'url', filename, filename)

    def dispatch(self, request, *args, **kwargs):
        super(UploadView, self).dispatch(request, *args, **kwargs)
        action = request.GET.get('action')
        if action in ['uploadimage', 'uploadvideo', 'uploadfile']:
            return self._action_upload(request)
        elif action == 'uploadscrawl':
            return self._action_scrawl(request)
        else:
            return self._json_result()


def send_file(request, filename):
    fp = open(os.path.join(UEDITOR_UPLOAD_PATH, filename), 'rb')
    response = FileResponse(fp)

    response['Content-Type'] = 'application/octet-stream'
    return response
