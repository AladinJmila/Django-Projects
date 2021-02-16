from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view

def apiOverview(request):

	return JsonResponse('API BASE POINT', safe=False)
