from django.shortcuts import render,HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin



class CourseOwnerMixin(LoginRequiredMixin,PermissionRequiredMixin):
    model = Course
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(instructor=self.request.user)

class CourseFormMixin(LoginRequiredMixin,PermissionRequiredMixin):
    model = Course
    fields = ['title','subject','overview','slug']
    template_name = "courses/manage/course/form.html"





class CourseListView(CourseOwnerMixin,ListView):
    template_name = "courses/manage/course/list.html"
    permission_required = "courses.view_course"

class CourseDetailView(CourseOwnerMixin,DetailView):
    template_name = "courses/manage/course/list.html"
    permission_required = "courses.view_course"

class CourseCreateView(CourseFormMixin,CreateView):
    permission_required = "courses.add_course"

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)

class CourseUpdateView(SuccessMessageMixin,CourseFormMixin,CourseOwnerMixin,UpdateView):
    permission_required = "courses.change_course"
    success_message = "updated successfully"


class CourseDeleteView(CourseOwnerMixin,DeleteView):
    permission_required = "courses.delete_course"
    template_name = "courses/manage/course/delete.html"
    success_url = reverse_lazy("courses:course-list")

    



def home(request): 
    return render(request,"home.html")
