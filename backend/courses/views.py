from django.shortcuts import render,HttpResponse
from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# Create your views here.

def home(request):
    return HttpResponse("hello world")




class home3(viewsets.ViewSet):

    def list(self):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Course.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CourseSerializer(user)
        return Response(serializer.data)


class home2(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer