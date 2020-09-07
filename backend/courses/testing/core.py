from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from courses.models import Course,Lesson,Week

class core:
    

    def __init__(self):
        self.set_instructor_owner()
        self.set_instructor_not_owner()
        self.set_student_enrolled()
        self.set_student_un_enrolled()

        self.course = self.create_course()


    def create_user(self,username,ins=False):
        client = APIClient()

        user = get_user_model().objects.create(username=username,password=12)
        user.set_password('123')
        user.is_instructor = ins
        user.is_student = not ins
        user.save()
        token = Token.objects.create(user=user)

        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return client

    
    def get_instructor_owner(self):
        return self.instructor_owner

    def get_instructor_not_owner(self):
        return self.instructor_not_owner

    def get_student_enrolled(self):
        return self.student_enrolled

    def get_student_un_enrolled(self):
        return self.student_un_enrolled



    def set_instructor_owner(self):
        self.instructor_owner =  self.create_user('instructor_owner',ins=True)

    def set_instructor_not_owner(self):
        self.instructor_not_owner =  self.create_user('instructor_not_owner',ins=True)

    def set_student_enrolled(self):
        self.student_enrolled =  self.create_user('student_enrolled')

    def set_student_un_enrolled(self):
        self.student_un_enrolled =  self.create_user('student_un_enrolled')



    def create_course(self):
        course = Course()
        course.title= "just_created"
        course.description = "course_desc"
        course.instructor_id = 1
        course.save()
        return course


