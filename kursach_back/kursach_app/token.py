from django.forms.models import model_to_dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.response import Response
import jwt
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError

from .models import User


class MyTokenObtainSerializer(TokenObtainPairSerializer):
    
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['is_staff'] = user.is_staff
        # ...

        return token
    

class MyTokenVerifyView(TokenViewBase):

    serializer_class = TokenVerifySerializer

    def post(self, request, *args, **kwargs):
        try:

            serializer = self.get_serializer(data=request.data)

            user_id = jwt.decode(request.data['token'], key='django-insecure-v96(ul6q_=kr!kmcj-rpu5@0n0&pa^0q&r$mtb1t9-4zwrhstn', algorithms='HS256')['user_id']

            user = User.objects.get(pk=user_id)

            try:
                serializer.is_valid(raise_exception=True)
            except TokenError as e:
                raise InvalidToken(e.args[0])

            return Response(model_to_dict(user, fields=['id', 'is_staff', 'username']))
        
        except InvalidSignatureError:
            return Response({'error': 'Токен не валиден'})
        
        except ExpiredSignatureError:
            return Response({'error': 'Срок жизни токена истёк'})
    

class MyTokenObtainPair(TokenViewBase):

    serializer_class = MyTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            user_name = request.data['username']

            user = User.objects.get(username=user_name)

            try:
                serializer.is_valid(raise_exception=True)
            except TokenError as e:
                raise InvalidToken(e.args[0])

            return Response(data={'token': serializer.validated_data, 'user':model_to_dict(user, fields=['id', 'is_staff', 'username'])})
        except:
            return Response({'error': 'Введены неверные данные'})