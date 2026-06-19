from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Course, Category
from .forms import CourseForm


def course_list(request):
    courses = Course.objects.all().order_by('-year', 'title')
    categories = Category.objects.all().order_by('name')

    category_id = request.GET.get('category')
    if category_id:
        courses = courses.filter(category_id=category_id)

    query = request.GET.get('q', '')
    if query:
        courses = courses.filter(
            Q(title__icontains=query) | Q(instructor__icontains=query)
        )

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'categories': categories,
        'query': query,
    })


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    courses = category.courses.all().order_by('-year', 'title')
    return render(request, 'courses/category_detail.html', {
        'category': category,
        'courses': courses,
    })


@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Add'})


def course_api(request):
    courses = Course.objects.all().order_by('-year', 'title')
    data = [
        {
            'id': course.pk,
            'title': course.title,
            'instructor': course.instructor,
            'credits': course.credits,
            'year': course.year,
            'semester': course.semester,
            'category': course.category.name,
        }
        for course in courses
    ]
    return JsonResponse(data, safe=False)