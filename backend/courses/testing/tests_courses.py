from django.test import TestCase
from rest_framework.test import APITestCase,APIRequestFactory
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from courses.models import Course,Lesson,Week

from .core import core


# Create your tests here.



class test_courses(APITestCase):
    
    def setUp(self):
        # self.app = APIRequestFactory()
        self.core = core()

        self.get_instructor_owner = self.core.get_instructor_owner();
        self.get_instructor_not_owner = self.core.get_instructor_not_owner();
        self.get_student_enrolled = self.core.get_student_enrolled();
        self.get_student_un_enrolled = self.core.get_student_un_enrolled();

 
    
    #------------------ #
    # -- course-list -- #
    #------------------ #
    """ 
        courese list allowed for any one even if not registered so only use client
    """

    def test_list_courses(self):
        course = self.core.course
        response = self.client.get(reverse('courses:course-list'),format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'],course.title)
        self.assertEqual(response.data[0]['description'],course.description)

    
    #-------------------- #
    # -- course-detail -- #
    #-------------------- #
    """ 
        courese detail allowed for any one even if not registered so only use client
    """

    def test_detail_courses(self):
        course = self.core.course
        response = self.client.get(reverse('courses:course-detail',args=[course.id]),format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['title'],course.title)
        self.assertEqual(response.data['description'],course.description)




    #-------------------- #
    # -- course-create -- #
    #-------------------- #
    """ 
        courese create allowed for any instructor 
        - instructor can
        - any student can't 
    """

    def test_create_courses_valid(self):
        data = {'title':'new_title','description':'new desc'}

        response = self.get_instructor_not_owner.post(reverse('courses:course-list'),format='json',data=data)
        
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'],data['title'])
        self.assertEqual(response.data['description'],data['description'])
        self.assertEqual(len(Course.objects.filter(id=response.data['id'])),1)

    def test_create_courses_failed(self):  
        data = {'title':'new_title','description':'new desc'}

        response = self.get_student_enrolled.post(reverse('courses:course-list'),format='json',data=data)

        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)




    #-------------------- #
    # -- course-update -- #
    #-------------------- #
    """ 
        courese update allowed for the owner only 
        - owner can
        - other instructor can't
        - registered students can't
        - other students can't 
    """

    def test_update_courses_valid(self):
        course = Course()
        course.title= "just_created"
        course.description = "course_desc"
        course.instructor_id = 1
        course.save()
        
        data = {'title':'new_title','description':'new desc'}

        response = self.get_instructor_owner.put(reverse('courses:course-detail',args=[course.id]),format='json',data=data)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['title'],data['title'])
        self.assertEqual(response.data['description'],data['description'])

    def test_update_courses_failed(self):
        course = self.core.course
        
        data = {'title':'new_title','description':'new desc'}

        responses=[]

        responses.append(self.get_instructor_not_owner.put(reverse('courses:course-detail',args=[course.id]),format='json',data=data))
        responses.append(self.get_student_enrolled.put(reverse('courses:course-detail',args=[course.id]),format='json',data=data))
        responses.append(self.get_student_un_enrolled.put(reverse('courses:course-detail',args=[course.id]),format='json',data=data))
        

        for response in responses:
            self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)


    #-------------------- #
    # -- course-delete -- #
    #-------------------- #

    """ 
        courese update allowed for the owner only 
        - owner can
        - other instructor can't
        - registered students can't
        - other students can't 
    """


    def test_delete_courses_valid(self):
        course = self.core.create_course()
        id = course.id
        response = self.get_instructor_owner.delete(reverse('courses:course-detail',args=[id]),format='json')
        
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Course.objects.filter(id=id)),0)

        

    def test_delete_courses_failed(self):
        course = self.core.create_course()
        
        responses=[]

        responses.append(self.get_instructor_not_owner.delete(reverse('courses:course-detail',args=[course.id]),format='json'))
        responses.append(self.get_student_enrolled.delete(reverse('courses:course-detail',args=[course.id]),format='json'))
        responses.append(self.get_student_un_enrolled.delete(reverse('courses:course-detail',args=[course.id]),format='json'))
        

        for response in responses:
            self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)



