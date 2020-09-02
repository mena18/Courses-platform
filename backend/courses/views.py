from django.shortcuts import render,HttpResponse
from rest_framework import viewsets,status
from rest_framework.views import APIView
from .models import Course,Lesson
from .serializers import CourseSerializer,LessonSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404


# Create your views here.

def home(request):
    return HttpResponse("hello world")




class list_courses(APIView):

    def get(self,request,format=None):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)


    def post(self,request,format=None):
        serializer = CourseSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class course_detail(APIView):
    
    def get_object(self,pk):
        try:
            return Course.objects.get(id=pk)
        except:
            raise Http404

    def get(self,request,pk,format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
        


class list_lessons(APIView):

    def get(self,request,course_id,format=None):
        queryset = Lesson.objects.filter(course__id=course_id)
        serializer = LessonSerializer(queryset, many=True)
        return Response(serializer.data)


    def post(self,request,course_id,format=None):
        serializer = LessonSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class lesson_detail(APIView):
    
    def get_object(self,pk):
        try:
            return Lesson.objects.get(id=pk)
        except:
            raise Http404

    def get(self,request,course_id,lesson_id,format=None):
        lesson = self.get_object(pk)
        serializer = LessonSerializer(Lesson)
        return Response(serializer.data)
        