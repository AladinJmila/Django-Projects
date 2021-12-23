from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import EmployeeSerializer
from django.http import HttpResponse

class EmployeeViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = EmployeeSerializer

def home(request):
  return HttpResponse('Hello employee manager.')