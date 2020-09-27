from django.shortcuts import render,HttpResponse,redirect
from django.conf import settings
# Create your views here.



from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from accounts.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from courses.models import User_registration,Course 



class StudentRegistrationView(CreateView):
    template_name = 'students/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('courses:student-course-list')

    def get(self,request,*args,**kwargs):
        if(request.user.is_authenticated):
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().get(request,*args,**kwargs)

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],password=cd['password1'])
        login(self.request, user)
        return result


from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from django.views.generic import FormView



class StudentEnrollCourseView(LoginRequiredMixin,FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self,form):
        self.course = form.cleaned_data['course']
        User_registration.objects.create(user=self.request.user,course=self.course,rating=0)        
        return super().form_valid(form)



    def get_success_url(self):
        return reverse_lazy("student_course_detail",args=[self.course.id])        


from django.views.generic import ListView
from django.views.generic.detail import DetailView

class StudentCourseListView(LoginRequiredMixin,ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__user__in=[self.request.user])





class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'


    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__user__in=[self.request.user])

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:

            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.first()
        return context


