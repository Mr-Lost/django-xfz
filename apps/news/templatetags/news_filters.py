from django import template
from datetime import datetime
import pytz
from django.utils.timezone import now as now_func, localtime

register = template.Library()

# 过滤器最多只能有两个参数
# 过滤器的第一个参数永远都是被过滤的那个参数(即竖线左边的那个参数)
# @register.filter('my_greet')
# def greet(value, word):
#     return value + word


@register.filter
def time_since(value):
    """
    timer距离现在的时间间隔
    1.如果时间间隔小于1分钟以内，那么就显示“刚刚”
    2.大于1分钟小于1小时，显示“xx分钟前”
    3.大于1小时小于24小时，显示“xx小时前”
    4.大于24小时小于30天，显示“xx天前”
    5.否则显示具体时间
    """
    if not isinstance(value, datetime):
        return value
    now = datetime.now()
    # offset-naive是不含时区的类型，而offset-aware是有时区类型，两者不能比较
    # now = now.replace(tzinfo=pytz.timezone('UTC'))
    now = now_func()

    timestamp = (now - value).total_seconds()
    if timestamp < 60:
        return '刚刚'
    elif 60 <= timestamp < 60*60:
        minutes = int(timestamp/60)
        return '%s分钟前' % minutes
    elif 60*60 <= timestamp < 60*60*24:
        hours = int(timestamp/60/60)
        return '%s小时前' % hours
    elif 60*60*24 <= timestamp < 60*60*24*30:
        days = int(timestamp/60/60/24)
        return '%s天前' % days
    else:
        return value.strftime('%Y/%m/%d %H:%M')


@register.filter
def time_format(value):
    if not isinstance(value, datetime):
        return value
    return localtime(value).strftime('%Y/%m/%d %H:%M:%S')   # 调用settings中的时区的时间
