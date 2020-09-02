from rest_framework import serializers
from .models import Course,Lesson


class LessonSerializer(serializers.ModelSerializer):
    
    course_id = serializers.CharField(source="course")
    course_title = serializers.CharField(source="course.title",read_only=True)

    # course_title = serializers.SerializerMethodField('get_course_name',read_only=True)
    # def get_course_name(self, obj):
    #     return obj.course.title


    # course_title = serializers.CharField(source="course.title")

    class Meta:
        model = Lesson
        fields = ['id','title','description','video_url','course_id','course_title']
        # extra_kwargs = {
        #     'course': {'view_name': 'course_id'}
        # }



 

class CourseSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id','title','description','lessons',)

