from django.urls import include, path
from api import views

urlpatterns = [
    path('clients/create', views.UserCreateAPIView.as_view(), name='user_create'),
]