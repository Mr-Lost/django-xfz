from django.db import models


class CourseCategory(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField(null=True, default=0)


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.URLField()
    position = models.CharField(max_length=100)
    profile = models.TextField()


class Course(models.Model):
    title = models.CharField(max_length=100)
    teacher = models.ForeignKey('Teacher', on_delete=models.DO_NOTHING)
    category = models.ForeignKey('CourseCategory', on_delete=models.DO_NOTHING)
    video_url = models.URLField()   # 默认最大长度200,本地视频名称最好用字母和数字
    cover_url = models.URLField()
    price = models.FloatField()
    pub_time = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()
    profile = models.TextField()
