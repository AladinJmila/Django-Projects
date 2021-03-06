from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from poll.models import *
from poll.serializers import QuestionSerializer, ChoiceSerializer
from rest_framework.parsers import JSONParser 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework import viewsets
from rest_framework.decorators import action


class PollViewSet(viewsets.ModelViewSet):
  serializer_class = QuestionSerializer
  queryset = Question.objects.all()
  lookup_field = 'id'

  @action(detail=True, methods=['GET'])
  def choices(self, request, id=None):
    question = self.get_object()
    choices = Choice.objects.filter(question=question)
    serializer = ChoiceSerializer(choices, many=True)
    return Response(serializer.data, status=200)

  @action(detail=True, methods=['POST'])
  def choice(self, request, id=None):
    question = sefl.get_object()
    data = request.data
    data['question'] = question.id
    serializer = QuestionSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


class PollListView(generics.GenericAPIView, 
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,):

  serializer_class = QuestionSerializer
  queryset = Question.objects.all()
  lookup_field = 'id'

  def get(self, request, id=None):
    if id:
      return self.retrieve(request, id)
    
    return self.list(request)

  def post(self, request):
    return self.create(request)

  def perform_create(self, serializer):
    serializer.save(created_by=self.request.user)

  def put(self, request, id=None):
    return self.update(request, id)

  def perform_update(self, serializer):
    serializer.save(created_by=self.request.user)

  def delete(self, request, id=None):
    return self.destroy(request, id)

class PollAPIView(APIView):
  def get(self, request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data, status=200)

  def post(self, request):
    data = request.data
    serializer = QuestionSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


class PollDetailAPIView(APIView):
  def get_object(self, id):
    try:
      return Question.objects.get(id=id)
    except Question.DoesNotEixst:
      return Response({'errors': 'Given question object not found.'}, status=404)

  def get(self, request, id=None):
    instance = self.get_object(id)
    serializer = QuestionSerializer(instance)
    return Response(serializer.data)
  
  def put(self, request, id=None):
    data = request.data
    instance = self.get_object(id)
    serializer = QuestionSerializer(instance, data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

  def delete(self, request, id=None):
    instance = self.get_object(id)
    instance.delete()
    return HttpResponse(status=204)


@csrf_exempt
def poll(request):
  if request.method == 'GET':
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return JsonResponse(serializer.data, safe=False)

  elif request.method == 'POST':
    data = JSONParser().parse(request)
    serializer = QuestionSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=201) # Created (Resource successfully created)
    return JsonResponse(serializer.errors, status=400) # Bad request


@csrf_exempt
def poll_details(request, id):
  try:
    instance = Question.objects.get(id=id)
  except Question.DoesNotExist:
    return JsonResponse({'errors': 'Given question object not found'},status=404)

  if request.method == 'GET':
    serializer = QuestionSerializer(instance)
    return JsonResponse(serializer.data)

  elif request.method == 'PUT':
    data = JSONParser().parse(request)
    serializer = QuestionSerializer(instance, data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=200) # Resource successfully updated
    return JsonResponse(serializer.errors, status=400) # Bad request

  elif request.method == 'DELETE':
    instance.delete()
    return HttpResponse(status=204) # No Content (resource successfully deleted) 


def index(request):
  questions = Question.objects.all()
  context = {
    'title': 'polls',
    'questions': questions
  }
  return render(request, 'polls/index.html', context)


def details(request, id=None):
  try:
    question = Question.objects.get(id=id)
  except:
    raise Http404
  context = {
    'title': 'polls',
    'question': question,
  }
  return render(request, 'polls/details.html', context)

# def poll(request, id=None):
#   if request.method == 'GET':
#     try:
#       question = Question.objects.get(id=id)
#     except: 
#       raise Http404
#     context = {
#       'question': question
#     }
#     return render(request, 'polls/poll.html', context)

#   if request.method == 'POST':
#     user_id = 1
#     print(request.POST)
#     data = request.POST # or can be request.data
#     answer = Answer.objects.create(user_id=user_id, choice_id=data['choice'])
#     if answer:
#       return HttpResponse('Your vote was done successfully.')
#     else: 
#       return HttpResponse('You vote was not done successfully.')
    
