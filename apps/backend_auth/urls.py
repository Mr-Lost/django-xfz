from django.urls import path
from . import views

app_name = 'backend_auth'

# 新闻相关
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('news_list/', views.NewsListView.as_view(), name='news_list'),
    path('news_edit/', views.NewsEditView.as_view(), name='news_edit'),
    path('news_delete/', views.news_delete, name='news_delete'),
    path('news_publish/', views.NewsPublishView.as_view(), name='news_publish'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('news_category/', views.news_category, name='news_category'),
    path('news_category_add/', views.news_category_add, name='news_category_add'),
    path('news_category_edit/', views.news_category_edit, name='news_category_edit'),
    path('news_category_delete/', views.news_category_delete, name='news_category_delete'),
    path('banners/', views.banners, name='banners'),
    path('banner_list/', views.banner_list, name='banner_list'),
    path('banner_add/', views.banner_add, name='banner_add'),
    path('banner_delete/', views.banner_delete, name='banner_delete'),
    path('banner_edit/', views.banner_edit, name='banner_edit'),
]

# 课程相关
urlpatterns += [
    path('course_publish/', views.CoursePublishView.as_view(), name='course_publish'),
    path('course_category/', views.course_category, name='course_category'),
    path('course_category_add/', views.course_category_add, name='course_category_add'),
    path('course_category_edit/', views.course_category_edit, name='course_category_edit'),
    path('course_category_delete/', views.course_category_delete, name='course_category_delete'),
]
