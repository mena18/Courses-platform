from rest_framework import permissions
from courses.models import Course,User_registration

class Course_permession(permissions.BasePermission):



    def has_permission(self, request, view):     
        if(view.action == 'create'):
            return request.user.is_instructor  

        return True

    def has_object_permission(self, request, view, obj):
        if(view.action == 'register' ):
            return request.user.is_student
        elif(view.action == 'rate' or view.action == 'weeks'):
            return obj.students.filter(user_id=request.user.id).exists()

        return request.user == obj.instructor or request.method == 'GET'
        


class IsOwnerOrStudent(permissions.BasePermission):


    def set_course(self,view):
        self.course = course = Course.objects.get(id=view.kwargs.get('course_id', None))

    def has_permission(self, request, view): 
        self.set_course(view)
        if(request.user == self.course.instructor):
            return True


        if(view.action == 'list' ):
            return User_registration.objects.filter(course_id=self.course.id,user_id=request.user.id).exists()
        if(view.action == 'create' ):
            return False
        
        return True


    def has_object_permission(self, request, view, obj):
        if(obj.course.instructor == request.user):
            return True

        
        if(view.action == 'retrieve' ):
            return obj.course.students.filter(user_id=request.user.id).exists()

        return False



        
