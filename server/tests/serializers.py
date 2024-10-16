from rest_framework import serializers
from .models import Answer, Question, Test


class AnswerSerialier(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["answer", "correctnes"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerialier(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["question", "answers"]

    def validate(self, attrs):
        answers = attrs.get('answers')
        if any(answers.get('correcntes') for answer in answers):
            raise ValueError("Question must have at least one correct answer")
        return super().validate(attrs)
    

class TestSerializer(serializers.ModelSerializer):
    question = QuestionSerializer
    class Meta:
        model = Test
        fileds = ["title"]

