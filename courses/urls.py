from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('new/', views.course_create, name='course_create'),
    path('api/courses/', views.course_api, name='course_api'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
]