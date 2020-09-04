from django.contrib import admin
from .models import Course,Lesson,User_registration,Week
# Register your models here.



admin.site.register(Course)
admin.site.register(Week)
admin.site.register(Lesson)
admin.site.register(User_registration)


