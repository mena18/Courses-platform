from django.urls import path,include
from .views import home,list_courses,course_detail,list_lessons,lesson_detail
from django.http import JsonResponse


app_name="courses"

urlpatterns = [
    path('', list_courses.as_view(),name="index"),
    path('<int:pk>/', course_detail.as_view(),name="detail"),
    path('<int:course_id>/lessons/', list_lessons.as_view(),name="lesson_index"),
    path('<int:course_id>/lessons/<int:lesson_id>/', lesson_detail.as_view(),name="lesson_detail"),

    
]

