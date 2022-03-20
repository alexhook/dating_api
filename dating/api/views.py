from .models import User
from .serializers import UserSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer


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
    

