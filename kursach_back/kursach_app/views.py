from django.shortcuts import render
from .models import Company, User
from .serializers import CompanySerializer, UserSerializer
from rest_framework import views
from rest_framework.response import Response

class UserAPIview(views.APIView):
    def get(self, request):
        data = User.objects.all().values()
        return Response(list(data))
    
    # def post(self, reuqest):



class CompanyAPIview(views.APIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer