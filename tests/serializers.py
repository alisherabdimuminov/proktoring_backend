from rest_framework import serializers

from users.serializer import UserModelSerializer
from users.models import User

from .models import Test, Set, Question


class SetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ("id", "name", )


class CreateSetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ("name", )

class QuestionModelSerializer(serializers.ModelSerializer):
    set = SetModelSerializer(Set)
    class Meta:
        model = Question
        fields = ("question", "answer_a", "answer_b", "answer_c", "answer_d", "correct_answer", "score", "set", )

class CreateQuestionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("set", "question", "answer_a", "answer_b", "answer_c", "answer_d", "correct_answer", "score", )


class TestsModelSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField("func_name")
    user = UserModelSerializer(User, many=False)
    set = SetModelSerializer(Set)

    def func_name(self, obj: Test):
        if not obj.questions.exists():
            questions = Question.objects.filter(set__pk=obj.set.pk).order_by("?")[:obj.questions_count]
            print(questions.all())
            for q in questions:
                obj.questions.add(q)
                print(obj.questions.all())
                print(q)
            obj.save()
            print(obj.questions.all())
        return obj.name

    class Meta:
        model = Test
        fields = ("uuid", "name", "user", "set", "passed_score", "status", "percentage", "elapsed", "questions_count", "left", "right", "two_person", "no_person", )


class CreateTestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ("name", "user", "set", "passed_score", "questions_count", )


class TestModelSerializer(serializers.ModelSerializer):
    questions = QuestionModelSerializer(Question, many=True)
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H-%M-%S")
    class Meta:
        model = Test
        fields = ("name", "user", "set", "status", "passed_score", "questions_count", "questions", "start_time", "cases", "percentage", )
