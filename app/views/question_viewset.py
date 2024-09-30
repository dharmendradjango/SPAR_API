from rest_framework import viewsets
from app.serilaizers.question_serializer import *

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionGroupViewSet(viewsets.ModelViewSet):
    queryset = QuestionGroup.objects.all()
    serializer_class = QuestionGroupSerializer
