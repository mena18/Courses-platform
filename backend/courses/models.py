from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator
from django.conf import settings
from django.db.models import Sum,Count
from django.db.models import Q
# Create your models here.

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.urls import reverse


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title



class Course(models.Model):
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="created_courses")
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    slug = models.SlugField()
    overview = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("courses:course-edit", kwargs={"pk": self.pk})
    


class Module(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()

    order = OrderField(blank=True,for_fields=['course'])
    

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.order)+" "+self.title



class Content(models.Model):
    module = models.ForeignKey(Module,related_name="contents",on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,limit_choices_to={'model__in':("text","video","image","file")})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type','object_id')

    order = OrderField(blank=True,for_fields=['Module'])


    class Meta:
        ordering = ['order']



class ItemBase(models.Model):
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="%(class)s_related")

    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta : 
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField()

class Video(ItemBase):
    url = models.URLField()

class Image(ItemBase):
    file = models.FileField(upload_to='images')



class User_registration(models.Model):
    course = models.ForeignKey(Course,related_name="students",on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="courses",on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator,MaxValueValidator])

    class Meta:
        index_together = [['user', 'course']]
        unique_together = [['user', 'course']]



# class Lesson(models.Model):
#     week = models.ForeignKey(Module,on_delete=models.CASCADE,related_name='lessons')
#     course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='lessons')
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True,null=True)
#     video_url = models.URLField()



    # def save(self, *args, **kwargs): 
    #     obj = User_registration.objects.filter(Q(course_id=self.course_id) & ~Q(rating=0) & ~Q(id=self.id)).aggregate(rate = Sum("rating"),counter=Count('rating'))
    #     obj['rate'] = 0 if obj['rate'] == None else obj['rate']
    #     self.course.rating =  (obj['rate']+int(self.rating)) / (obj['counter']+1)
    #     self.course.save()
    #     return super(User_registration, self).save(*args, **kwargs)
