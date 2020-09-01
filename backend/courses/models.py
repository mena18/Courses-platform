from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.



class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    category = models.CharField(max_length=50)
    published_at = models.DateTimeField(auto_now_add=True)
    
    # image = models.ImageField()
    


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    video_url = models.URLField()


class User_registration(models.Model):
    course = models.ForeignKey(Course,related_name="students",on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="courses",on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator,MaxValueValidator])

    class Meta:
        index_together = [['user', 'course']]
        unique_together = [['user', 'course']]