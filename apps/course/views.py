from django.shortcuts import render
from .models import Course, Teacher, CourseCategory


def course_index(request):
    courses = Course.objects.all()
    categories = CourseCategory.objects.all()
    teachers = Teacher.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'course/index.html', context=context)


def course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    context = {
        'course': course,
    }
    return render(request, 'course/detail.html', context=context)
