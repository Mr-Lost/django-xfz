from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.views.decorators.http import require_POST, require_GET
from apps.news.models import NewsCategory, News, Banner
from apps.course.models import Course, CourseCategory, Teacher
from utils import restful
from .forms import NewsCategoryEditForm, NewsPublishForm, BannerForm, EditBannerForm, NewsEditForm, CoursePublishForm
import os
from django.conf import settings
from apps.news.serializers import BannerSerializer
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse


@staff_member_required(login_url='index')
def index(request):
    return render(request, 'xfz_backend/index.html')


def login_view(request):
    return render(request, 'xfz_backend/login.html')


class NewsListView(View):
    def get(self, request):
        page = int(request.GET.get('p', 1))

        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category', 0))   # request.GET.get(arg, default)返回的是字符串

        newses = News.objects.select_related('category', 'author')

        # 查询功能
        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2019, month=10, day=1)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            newses = newses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))   # received a naive datetime (2019-12-02 00:00:00) while time zone support is active
        if title:
            newses = newses.filter(title__icontains=title)   # 忽略大小写
        if category_id:
            newses = newses.filter(category=category_id)

        paginator = Paginator(newses, 2)
        page_obj = paginator.page(page)
        context_data = self.get_pagination_data(paginator, page_obj)
        context = {
            'categories': NewsCategory.objects.all(),
            'newses': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'start': start,
            'end': end,
            'title': title,
            'category_id': category_id,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or 0
            }),
        }
        context.update(context_data)
        return render(request, 'xfz_backend/news_list.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page+1, num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1, current_page+around_count+1)

        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


class NewsEditView(View):
    def get(self, request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(pk=news_id)
        categories = NewsCategory.objects.all()
        context = {
            'news': news,
            'categories': categories
        }
        return render(request, 'xfz_backend/news_publish.html', context=context)

    def post(self, request):
        form = NewsEditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            pk = form.cleaned_data.get('pk')
            News.objects.filter(pk=pk).update(title=title, desc=desc, thumbnail=thumbnail,
                                              content=content, category=category)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_POST
def news_delete(request):
    news_id = request.POST.get('news_id')
    News.objects.filter(pk=news_id).delete()
    return restful.ok()


class NewsPublishView(View):
    def get(self, request):
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'xfz_backend/news_publish.html', context=context)

    def post(self, request):
        form = NewsPublishForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category_id')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.create(title=title, desc=desc, content=content, thumbnail=thumbnail,
                                category=category, author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_POST
def upload_file(request):
    file = request.FILES.get('file')
    folder = request.POST.get('folder')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, folder, name), 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    url = request.build_absolute_uri((settings.MEDIA_URL+'%s/'+name) % folder)
    return restful.result(data={'url': url})


@require_GET
def news_category(request):
    categories = NewsCategory.objects.all()
    print(categories)
    newses = News.objects.all()
    dic = {}
    for category in categories:
        dic[category.pk] = 0
    for news in newses:
        category = news.category.pk
        dic[category] += 1
    for i in dic:
        NewsCategory.objects.filter(pk=i).update(amount=dic[i])
    context = {
        'categories': categories
    }
    return render(request, 'xfz_backend/news_category.html', context=context)


@require_POST
def news_category_add(request):
    name = request.POST.get('name')
    exists = NewsCategory.objects.filter(name=name).exists()
    if not exists:
        NewsCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已经存在！')


@require_POST
def news_category_edit(request):
    form = NewsCategoryEditForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            NewsCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message='该分类不存在！')
    else:
        return restful.params_error(message=form.get_errors())


@require_POST
def news_category_delete(request):
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        restful.unauth(message='该分类不存在！')


def banners(request):
    return render(request, 'xfz_backend/banner.html')


def banner_add(request):
    form = BannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        link_to = form.cleaned_data.get('link_to')
        image_url = form.cleaned_data.get('image_url')
        banner = Banner.objects.create(priority=priority, link_to=link_to, image_url=image_url)
        return restful.result(data={'banner_id': banner.pk})
    else:
        return restful.params_error(message=form.get_errors())


def banner_list(request):
    banner = Banner.objects.all()
    serializer = BannerSerializer(banner, many=True)
    return restful.result(data=serializer.data)


def banner_delete(request):
    banner_id = request.POST.get('banner_id')
    Banner.objects.filter(pk=banner_id).delete()
    return restful.ok()


def banner_edit(request):
    form = EditBannerForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        priority = form.cleaned_data.get('priority')
        link_to = form.cleaned_data.get('link_to')
        image_url = form.cleaned_data.get('image_url')
        Banner.objects.filter(pk=pk).update(image_url=image_url, priority=priority, link_to=link_to)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())


class CoursePublishView(View):
    def get(self, request):
        context = {
            'categories': CourseCategory.objects.all(),
            'teachers': Teacher.objects.all()
        }
        return render(request, 'xfz_backend/course_publish.html', context=context)

    def post(self, request):
        form = CoursePublishForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            teacher_id = form.cleaned_data.get('teacher_id')
            teacher = Teacher.objects.get(pk=teacher_id)
            category_id = form.cleaned_data.get('category_id')
            category = CourseCategory.objects.get(pk=category_id)
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get('cover_url')
            price = form.cleaned_data.get('price')
            profile = form.cleaned_data.get('profile')
            duration = form.cleaned_data.get('duration')
            print(teacher, category)
            Course.objects.create(title=title, teacher=teacher, category=category, video_url=video_url,
                                  cover_url=cover_url, price=price, profile=profile, duration=duration)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_GET
def course_category(request):
    categories = CourseCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'xfz_backend/course_category.html', context)


@require_POST
def course_category_add(request):
    name = request.POST.get('name')
    exists = CourseCategory.objects.filter(name=name).exists()
    if not exists:
        CourseCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已存在！')


@require_POST
def course_category_edit(request):
    pass


@require_POST
def course_category_delete(request):
    pass

