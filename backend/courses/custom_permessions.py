from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):



    def has_permission(self, request, view):     
        if(view.action == 'create'):
            return request.user.is_instructor  
        return True

    def has_object_permission(self, request, view, obj):
        if(view.action == 'register' ):
            return request.user.is_student   

        return request.user == obj.instructor or request.method == 'GET'
        




        
