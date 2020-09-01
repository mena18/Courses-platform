from django.urls import path,include
from .views import home,home2,home3
from rest_framework import routers
from django.http import JsonResponse

router = routers.DefaultRouter()
router.register("home2",home2)
router.register("home3",home3)


urlpatterns = [
    path('home/', home,name="home"),
    # path('home2/',home2,name='home2')
    # path('home3/', home3,name="home3"),   
    path('', include(router.urls)),    
    
]

