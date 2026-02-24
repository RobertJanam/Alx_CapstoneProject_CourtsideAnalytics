from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_page, name='login-page'),
]