from django.shortcuts import render,HttpResponse
from rest_framework import viewsets,status
from rest_framework.views import APIView
from .models import Course,Lesson,Week
from .serializers import CourseSerializer,LessonSerializer,WeekSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.decorators import action



from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework import permissions
from .custom_permessions import IsOwnerOrReadOnly
from rest_framework.authtoken.models import Token

# Create your views here.

def home(request):
    return HttpResponse("hello world")


class courses_view(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]


    def create(self,request):
        ser = self.serializer_class(data=request.data)
        if(ser.is_valid()):
            ser.save(instructor=request.user)
            return Response(ser.data,status=status.HTTP_200_OK)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)



    @action(detail=True,methods=['POST'])
    def register(self,request,pk=None):
        res = self.serializer_class(self.get_object())
        return Response({'sucess':'user registerd in this course','course details':res.data},status=status.HTTP_200_OK)


    @action(detail=True,methods=['PATCH'])
    def rate(self,request,pk=None):
        res = self.serializer_class(self.get_object())
        return Response({'sucess':'rating courses','course details':res.data},status=status.HTTP_200_OK)


    @action(detail=True,methods=['GET'])
    def students(self,request,pk=None):
        res = self.serializer_class(self.get_object())
        return Response({'sucess':'all students','course details':res.data},status=status.HTTP_200_OK)


    @action(detail=True,methods=['GET'])
    def weeks(self,request,pk=None):
        res = self.serializer_class(self.get_object())
        return Response({'sucess':'all students','course details':res.data},status=status.HTTP_200_OK)





class weeks_view(viewsets.ModelViewSet):
    serializer_class = WeekSerializer
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Week.objects.filter(course_id = course_id)

    # def create(self,request,course_id=None,pk=None):
    #     ser = self.serializer_class(data=request.data)
    #     if(ser.is_valid()):
    #         ser.save(course_id=course_id)
    #         return Response(ser.data)
    #     return Response(ser.errors)
        
    
    def create(self,request,course_id=None):
        ser = self.serializer_class(data=request.data)
        if(ser.is_valid()):
            try:
                ser.save(course_id=course_id)
            except:
                return Response({'detail':"course is not Found"},status=status.HTTP_404_NOT_FOUND) 
            
            return Response(ser.data)
        return Response(ser.errors)
    



class lessons_view(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lesson.objects.filter(course_id = course_id)

    # def create(self,request,course_id=None,pk=None):
    #     ser = self.serializer_class(data=request.data)
    #     if(ser.is_valid()):
    #         ser.save(course_id=course_id)
    #         return Response(ser.data)
    #     return Response(ser.errors)
        
    
    def create(self,request,course_id=None,week_id=None):
        ser = self.serializer_class(data=request.data)
        if(ser.is_valid()):
            try:
                ser.save(course_id=course_id,week_id=week_id)
            except:
                return Response({'detail':"course or week is not Found"},status=status.HTTP_404_NOT_FOUND)    
            return Response(ser.data)
        return Response(ser.errors)
    




# User


from .serializers import UserSerializer

class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer




# class list_courses(APIView):

#     def get(self,request,format=None):
#         queryset = Course.objects.all()
#         serializer = CourseSerializer(queryset, many=True)
#         return Response(serializer.data)


#     def post(self,request,format=None):
#         serializer = CourseSerializer(data=request.data)
#         if (serializer.is_valid()):
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

# class course_detail(APIView):
    
#     def get_object(self,pk):
#         try:
#             return Course.objects.get(id=pk)
#         except:
#             raise Http404

#     def get(self,request,pk,format=None):
#         course = self.get_object(pk)
#         serializer = CourseSerializer(course)
#         return Response(serializer.data)
        


# class list_lessons(APIView):

#     def get(self,request,course_id,format=None):
#         queryset = Lesson.objects.filter(course__id=course_id)
#         serializer = LessonSerializer(queryset, many=True)
#         return Response(serializer.data)


#     def post(self,request,course_id,format=None):
#         serializer = LessonSerializer(data=request.data)
#         if (serializer.is_valid()):
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

# class lesson_detail(APIView):
    
#     def get_object(self,pk):
#         try:
#             return Lesson.objects.get(id=pk)
#         except:
#             raise Http404

#     def get(self,request,course_id,lesson_id,format=None):
#         lesson = self.get_object(pk)
#         serializer = LessonSerializer(Lesson)
#         return Response(serializer.data)
        