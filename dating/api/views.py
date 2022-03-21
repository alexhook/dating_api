from .models import User
from .serializers import UserSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import  PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as dj_filters
from .utils import great_circle
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer

class UserListFilter(dj_filters.FilterSet):
    distance = dj_filters.NumberFilter(label='Distance', method='filter_distance')

    class Meta:
        model = User
        fields = ['gender', 'distance']

    def filter_distance(self, queryset, name, value):
        current_user = self.request.user
        lat1 = current_user.latitude
        lon1 = current_user.longitude

        ids = []

        for user in queryset:
            if great_circle(lat1, lon1, user.latitude, user.longitude) <= value:
                ids.append(user.id)
        
        return queryset.filter(id__in=ids)

class UserListViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = UserListFilter
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)


MATCH_EMAIL_SUBJECT = 'Вы кому-то понравились!'
MATCH_EMAIL_TEMPLATE = 'api/match_email.html'

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_match(request: Request, id: int):
    try:
        to_user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=404)
    
    from_user = request.user
    like = from_user.likes.filter(id=to_user.id)
    if like.exists():
        return Response(status=409)

    if from_user != to_user:
        from_user.likes.add(to_user)
        match = to_user.likes.filter(id=from_user.id)
        if match.exists():
            to_user.email_user(
                MATCH_EMAIL_SUBJECT,
                message=render_to_string(
                    MATCH_EMAIL_TEMPLATE,
                    {
                        'name': from_user.first_name,
                        'email': from_user.email
                    }
                )
            )
            from_user.email_user(
                MATCH_EMAIL_SUBJECT,
                message=render_to_string(
                    MATCH_EMAIL_TEMPLATE,
                    {
                        'name': to_user.first_name,
                        'email': to_user.email
                    }
                )
            )
            return Response({'email': to_user.email})
        return Response(status=201)
    return Response(status=409)
    

