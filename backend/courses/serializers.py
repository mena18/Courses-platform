from rest_framework import serializers
from .models import Course,Lesson,Week
from django.contrib.auth import get_user_model


class LessonSerializer(serializers.ModelSerializer):
    
    course_id = serializers.CharField(source="course",read_only=True)
    course_title = serializers.CharField(source="course.title",read_only=True)
    
    # course_title = serializers.SerializerMethodField('get_course_name',read_only=True)
    # def get_course_name(self, obj):
    #     return obj.course.title


    # course_title = serializers.CharField(source="course.title")

    class Meta:
        model = Lesson
        fields = ['id','title','description','video_url','course_id','course_title','week']
        extra_kwargs = {
            'week': {'read_only': True}
        }



class WeekSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Week
        fields = ('id','name','num','lessons',)


 

class CourseSerializer(serializers.ModelSerializer):

    weeks = WeekSerializer(many=True, read_only=True)
    # rating = serializers.CharField(source='get_rating',read_only=True)

    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=get_user_model.objects.all())
    instructor = serializers.ReadOnlyField(source="instructor.username")

    class Meta:
        model = Course
        fields = ('id','title','description','instructor','weeks','rating')

        extra_kwargs = {
            'instructor':{'read_only':True},
        }



class UserSerializer(serializers.ModelSerializer):
    created_courses = serializers.PrimaryKeyRelatedField(many=True,queryset = Course.objects.all())

    class Meta:
        model = get_user_model()
        fields = ['id','username','created_courses']    



class StudentSerializer(serializers.ModelSerializer):
    # created_courses = serializers.PrimaryKeyRelatedField(many=True,queryset = Course.objects.all())

    class Meta:
        model = get_user_model()
        fields = ['id','username']    