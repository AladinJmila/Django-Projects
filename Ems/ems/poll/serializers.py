from rest_framework import serializers
from poll.models import Question, Choice

class QuestionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Question
    fields = [
      'id',
      'title',
      'status',
      'created_by'
    ]

class ChoiceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Choice
    fields = '__all__'