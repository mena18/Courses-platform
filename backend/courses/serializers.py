from rest_framework import serializers
from .models import Course,Lesson,Week


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

    class Meta:
        model = Course
        fields = ('id','title','description','weeks',)

