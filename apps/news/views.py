from django.shortcuts import render, Http404
from .models import NewsCategory, News, Comments, Banner
from django.conf import settings
from .serializers import NewsSerializer, CommentSerializer
from utils import restful
from .forms import PublishCommentForm
from apps.xfz_auth.decorators import xfz_login_required


def index(request):
    count = settings.INDEX_NEWS_PER_PAGE
    newses = News.objects.select_related('category', 'author').all()[:count]   # 优化数据库查询性能，提前查找外键
    categories = NewsCategory.objects.all()
    context = {
        'newses': newses,
        'categories': categories,
        'banners': Banner.objects.all()
    }
    return render(request, 'news/index.html', context=context)


def news_pages(request):
    # 通过p参数指定获取第几页的数据，p参数通过查询字符串传过来/news/news_page/?p=1
    page = int(request.GET.get('p', 1))
    # 0代表不分类，直接按时间倒序排序
    category_id = int(request.GET.get('category_id', 0))
    start = (page - 1)*settings.INDEX_NEWS_PER_PAGE
    end = start + settings.INDEX_NEWS_PER_PAGE
    if category_id == 0:
        newses = News.objects.select_related('category', 'author').all()[start:end]
    else:
        newses = News.objects.select_related('category', 'author').filter(category__id=category_id)[start:end]
    serializer = NewsSerializer(newses, many=True)
    data = serializer.data
    return restful.result(data=data)


def news_detail(request, news_id):
    try:
        # 优化sql性能
        news = News.objects.select_related('category', 'author').prefetch_related('comments__author').get(pk=news_id)
        context = {
            'news': news
        }
        return render(request, 'news/detail.html', context=context)
    except News.DoesNotExist:
        raise Http404


@xfz_login_required
def publish_comment(request):
    form = PublishCommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        news_id = form.cleaned_data.get('news_id')
        news = News.objects.get(pk=news_id)
        comment = Comments.objects.create(content=content, news=news, author=request.user)
        serializer = CommentSerializer(comment)
        return restful.result(data=serializer.data)
    else:
        return restful.params_error(message=form.get_errors())


def search(request):
    return render(request, 'search/search.html')


def login_view(request):
    return render(request, 'common/auth.html')
