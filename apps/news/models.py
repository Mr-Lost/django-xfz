from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('NewsCategory', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('xfz_auth.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-pub_time']


class NewsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    amount = models.IntegerField(null=True, default=0)


class Comments(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('xfz_auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']


class Banner(models.Model):
    priority = models.IntegerField(default=0)
    image_url = models.URLField()
    link_to = models.URLField()
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority']
