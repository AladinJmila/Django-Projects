from django.shortcuts import render
from django.http import Http404
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