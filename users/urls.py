from django.urls import path
from .views import Register, LoginView

urlpatterns = [
    path('auth/signup', Register.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login')
]