from django.urls import path,include
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()


router.register('',views.courses_view,basename='course')
# router.register(r'{course_id}/lessons/$',views.lessons_view,basename='lesson')



# urlpatterns = router.urls

app_name='courses'


# course_list = views.courses_view.as_view({'get':'list','post':'create'})
# course_detail = views.courses_view.as_view({ 'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'})

week_list = views.weeks_view.as_view({'get':'list','post':'create'})
week_detail = views.weeks_view.as_view({ 'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'})


lesson_list = views.lessons_view.as_view({'get':'list','post':'create'})
lesson_detail = views.lessons_view.as_view({ 'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'})



urlpatterns = [
    # path('', list_courses.as_view(),name="index"),
    # path('<int:pk>/', course_detail.as_view(),name="detail"),
    # path('<int:course_id>/lessons/', list_lessons.as_view(),name="lesson_index"),
    # path('<int:course_id>/lessons/<int:lesson_id>/', lesson_detail.as_view(),name="lesson_detail"),

    # path('',course_list,name='course_list'),
    # path('<int:pk>/',course_detail,name='course_detail'),

    path('<int:course_id>/weeks/',week_list,name='week_list'),
    path('<int:course_id>/weeks/<int:pk>',week_detail,name='week_detail'),

    path('<int:course_id>/weeks/<int:week_id>/lessons/',lesson_list,name='lesson_list'),
    path('lessons/<int:pk>',lesson_detail,name='lesson_detail'),

    path('',include(router.urls)),

]

