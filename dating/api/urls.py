from django.urls import path
from api import views


urlpatterns = [
    path('clients/<int:id>/match', views.check_match, name='match'),
    path('clients/create', views.UserCreateAPIView.as_view(), name='create_user'),
    path('list', views.UserListViewSet.as_view({'get':'list'}), name='list'),
]