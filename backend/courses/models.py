from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator
from django.conf import settings
from django.db.models import Sum,Count
from django.db.models import Q
# Create your models here.



class Course(models.Model):
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="created_courses")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    category = models.CharField(max_length=50)
    published_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)



    # image = models.ImageField()

    def __str__(self):
        return str(self.id)
    


class Week(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='weeks')
    name = models.CharField(max_length=200,blank=True,null=True)
    num = models.IntegerField()


    def __str__(self):
        return self.name if self.name else str(self.num)


class Lesson(models.Model):
    week = models.ForeignKey(Week,on_delete=models.CASCADE,related_name='lessons')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    video_url = models.URLField()


class User_registration(models.Model):
    course = models.ForeignKey(Course,related_name="students",on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="courses",on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator,MaxValueValidator])

    class Meta:
        index_together = [['user', 'course']]
        unique_together = [['user', 'course']]



    def save(self, *args, **kwargs): 
        obj = User_registration.objects.filter(Q(course_id=self.course_id) & ~Q(rating=0) & ~Q(id=self.id)).aggregate(rate = Sum("rating"),counter=Count('rating'))
        obj['rate'] = 0 if obj['rate'] == None else obj['rate']
        self.course.rating =  (obj['rate']+int(self.rating)) / (obj['counter']+1)
        self.course.save()
        return super(User_registration, self).save(*args, **kwargs)
