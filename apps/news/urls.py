from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('<int:news_id>/', views.news_detail, name='detail'),
    path('search/', views.search, name='search'),
    path('login/', views.login_view, name='login'),
    path('news_page/', views.news_pages, name='news_page'),
    path('publish_comment/', views.publish_comment, name='publish_comment'),
]
