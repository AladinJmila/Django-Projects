from django.shortcuts import render
from django.http import Http404, HttpResponse
from poll.models import *

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

def poll(request, id=None):
  if request.method == 'GET':
    try:
      question = Question.objects.get(id=id)
    except: 
      raise Http404
    context = {
      'question': question
    }
    return render(request, 'polls/poll.html', context)

  if request.method == 'POST':
    user_id = 1
    print(request.POST)
    data = request.POST # or can be request.data
    answer = Answer.objects.create(user_id=user_id, choice_id=data['choice'])
    if answer:
      return HttpResponse('Your vote was done successfully.')
    else: 
      return HttpResponse('You vote was not done successfully.')
    
