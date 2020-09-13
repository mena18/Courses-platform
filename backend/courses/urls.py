from django.urls import path,include
from . import views

app_name = "courses"

urlpatterns = [
    
    path("courses/",views.CourseListView.as_view(),name="course-list"),
    # path("courses/<int:pk>",views.CourseDetailView.as_view(),name="course-detail"),
    path("courses/create",views.CourseCreateView.as_view(),name="course-create"),
    path("courses/<int:pk>/update",views.CourseUpdateView.as_view(),name="course-edit"),
    path("courses/<int:pk>/delete",views.CourseDeleteView.as_view(),name="course-delete"),

    path("courses/module/<int:id>",views.CourseListView.as_view(),name="module_content_list"),
    path("courses/courses/edit-module/<int:id>",views.CourseListView.as_view(),name="course-module_update"),
    path("",views.home,name="home"),

]