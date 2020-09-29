from django.contrib import admin
from .models import Course,Subject,User_registration,Module
# Register your models here.



@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title','slug')
    prepopulated_fields = {"slug":('title',)}


class Moduleinline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title','subject','created']
    list_filter = ['created','subject']
    search_fields = ['title','overview']
    prepopulated_fields = {"slug":('title',)}
    inlines = [Moduleinline]


admin.site.register(User_registration)

admin.site.index_template = "memcache_status/admin_index.html"


def call(s):
    print(s)


def func():
    start_time = time.time()
    call(Course.objects.all())
    return time.time() - start_time


def func2():
    start_time = time.time()
    courses = cache.get('courses')
    if not courses:
        courses = Course.objects.all()
        cache.set('courses',courses,300)
    call(courses)
    return time.time() - start_time