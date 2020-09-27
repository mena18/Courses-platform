from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.views.generic.base import TemplateResponseMixin,View
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView
from .models import Course,Module,Content,Subject
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .froms import ModuleFormSet
from django.apps import apps
from django.forms.models import modelform_factory

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin




# -----------------
# instructor views
# -----------------


class CourseOwnerMixin(LoginRequiredMixin,PermissionRequiredMixin):
    model = Course
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(instructor=self.request.user)

class CourseFormMixin(LoginRequiredMixin,PermissionRequiredMixin):
    model = Course
    fields = ['title','subject','overview','slug']
    template_name = "courses/manage/course/form.html"





class CourseManageListView(CourseOwnerMixin,ListView):
    template_name = "courses/manage/course/list.html"
    permission_required = "courses.view_course"

# class CourseDetailView(CourseOwnerMixin,DetailView):
#     template_name = "courses/manage/course/list.html"
#     permission_required = "courses.view_course"

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



class CourseModuleUpdateView(TemplateResponseMixin,View):
    template_name = "courses/manage/module/formset.html"
    course = None

    def get_formset(self,data=None):
        return ModuleFormSet(instance=self.course,data=data)
    
    def dispatch(self,request,pk):
        self.course = get_object_or_404(Course,id=pk,instructor=request.user)
        return super().dispatch(request,pk)


    def get(self,*args,**kwargs):
        formset = self.get_formset()
        return self.render_to_response({"course":self.course,"formset":formset})


    def post(self,request,*args,**kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("courses:course-list")
        return self.render_to_response({'course':self.course,"formset":formset})


class ContentCreateUpdateView(TemplateResponseMixin,View):
    module = None
    model = None
    obj = None
    template_name = "courses/manage/content/form.html"

    def get_model(self,model_name=None):
        if (model_name in ['text','video','image','file']):
            return apps.get_model(app_label='courses',model_name=model_name)
        return None

    def get_form(self,model,*args,**kwargs):
        form = modelform_factory(model,exclude=['instructor','order','created','updated'])
        return form(*args,**kwargs)
    
    def dispatch(self, request,module_id,model_name,id=None):
        self.module = get_object_or_404(Module,id=module_id,course__instructor=request.user)
        self.model = self.get_model(model_name)

        if(id):
            self.obj = get_object_or_404(self.model,id=id,instructor=request.user)

        return super().dispatch(request,module_id,model_name,id)
    

    def get(self,request,module_id,model_name,id=None):
        form = self.get_form(self.model,instance=self.obj)
        return self.render_to_response({'form':form,"object":self.obj})

    def post(self,request,module_id,model_name,id=None):
        form = self.get_form(self.model,instance=self.obj,data=request.POST,files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.instructor = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module,item=obj)
            return redirect('courses:module-content-list',self.module.id)
        return self.render_to_response({'form':form,'object':self.obj})
        

class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content,
        id=id,
        module__course__instructor=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('courses:module-content-list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'
    def get(self, request, module_id):
        module = get_object_or_404(Module,
        id=module_id,
        course__instructor=request.user)
        return self.render_to_response({'module': module})




class ModuleOrderView(CsrfExemptMixin,JsonRequestResponseMixin,View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,course__instructor=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})



class ContentOrderView(CsrfExemptMixin,JsonRequestResponseMixin,View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,module__course__instructor=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})






# -----------------
# Student views
# -----------------

from django.db.models import Count

class CourseListView(TemplateResponseMixin,View):
    model = Course
    template_name = "courses/course/list.html"

    def get(self,request,subject=None):
        subjects = Subject.objects.annotate(total_courses=Count('courses'))
        courses = Course.objects.annotate(total_modules=Count('modules'))
        if(subject):
            subject = get_object_or_404(Subject,slug=subject)
            courses = Course.objects.filter(subject = subject)
        return self.render_to_response({"subjects":subjects,"subject":subject,"courses":courses})


from students.forms import CourseEnrollForm

class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course/detail.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course':self.object})

        return context


def home(request): 
    return render(request,"home.html")
