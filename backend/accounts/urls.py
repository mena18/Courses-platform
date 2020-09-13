from django.urls import path,include
from django.contrib.auth import views as auth_view


app_name="accounts"

urlpatterns = [
    path('login/',auth_view.LoginView.as_view(redirect_authenticated_user=True),name="login"),
    path('logout/',auth_view.LogoutView.as_view(),name="logout"),
]
