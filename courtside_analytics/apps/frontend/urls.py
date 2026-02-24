from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('test/', views.test, name='test'),
    path('login/', views.login_page, name='login-page'),
    path('register/', views.register_page, name='register-page'),
]