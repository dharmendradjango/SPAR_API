from rest_framework import serializers
from app.models.question_model import *

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuestionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionGroup
        fields = '__all__'
