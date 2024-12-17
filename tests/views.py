import random
from datetime import datetime, timezone
from fpdf import FPDF

from django.http import HttpRequest, HttpResponse
from rest_framework import generics
from rest_framework import decorators
from rest_framework import permissions
from rest_framework.response import Response

from utils.translate import cyrillic_to_latin
from users.models import User

from .models import Question, Set, Test
from .serializers import (
    TestsModelSerializer, 
    QuestionModelSerializer, 
    SetModelSerializer,
    CreateTestModelSerializer,
    CreateQuestionModelSerializer,
    CreateSetModelSerializer,
    TestModelSerializer,
)


class PDF(FPDF):
    def header(self):
        # Rendering logo:
        self.image("logo.png", 5, 5, 15)
        self.set_font("helvetica", "B", 15)
        self.cell(80)
        self.cell(30, 10, "O'zbekiston-Finlandiya Pedagogika Instituti.", align="L")
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Platform powered by Ali", align="C")

# LIST

class TestsListAPIView(generics.ListAPIView):
    queryset = Test.objects.all().order_by("-id")
    serializer_class = TestsModelSerializer


class QuestionListAPIView(generics.ListAPIView):
    queryset = Question.objects.all().order_by("-id")
    serializer_class = QuestionModelSerializer


class SetsListAPIView(generics.ListAPIView):
    queryset = Set.objects.all().order_by("-id")
    serializer_class = SetModelSerializer


# ADD

@decorators.api_view(http_method_names=["POST"])
def add_test(request: HttpRequest):
    test = CreateTestModelSerializer(data=request.data)
    print(request.data)
    if test.is_valid():
        print(test.validated_data)
        test.create(test.validated_data)
        return Response({
            "status": "success",
            "code": "201",
            "data": None
        })
    print(test.errors)
    return Response({
        "status": "error",
        "code": "400",
        "data": None
    })


@decorators.api_view(http_method_names=["POST"])
def add_question(request: HttpRequest):
    question = CreateQuestionModelSerializer(data=request.data)
    print(request.data)
    if question.is_valid():
        question.create(question.validated_data)
        return Response({
            "status": "success",
            "code": "201",
            "data": None
        })
    print(question.errors)
    return Response({
        "status": "error",
        "code": "400",
        "data": None
    })


@decorators.api_view(http_method_names=["POST"])
def add_set(request: HttpRequest):
    Set = CreateSetModelSerializer(data=request.data)
    if Set.is_valid():
        Set.create(Set.validated_data)
        return Response({
            "status": "success",
            "code": "201",
            "data": None
        })
    return Response({
        "status": "error",
        "code": "400",
        "data": None
    })

# EDIT

def edit_test(request: HttpRequest, pk: int):
    test_obj = Test.objects.get(pk=pk)
    test = CreateTestModelSerializer(test_obj, data=request.data)
    if test.is_valid():
        test.create(test.validated_data)
        return Response({
            "status": "success",
            "code": "201",
            "data": None
        })
    return Response({
        "status": "error",
        "code": "400",
        "data": None
    })

@decorators.api_view(http_method_names=["POST"])
def edit_question(request: HttpRequest, pk: int):
    question_obj = Question.objects.get(pk=pk)
    question = CreateQuestionModelSerializer(question_obj, data=request.data)
    if question.is_valid():
        question.create(question.validated_data)
        return Response({
            "status": "success",
            "code": "201",
            "data": None
        })
    return Response({
        "status": "error",
        "code": "400",
        "data": None
    })

@decorators.api_view(http_method_names=["POST"])
def edit_set(request: HttpRequest, pk: int):
    Set_obj = Set.objects.get(pk=pk)
    Set = CreateSetModelSerializer(Set_obj, data=request.data)
    if Set.is_valid():
        Set.create(Set.validated_data)
        return Response({
            "status": "success",
            "code": "201",
            "data": None
        })
    return Response({
        "status": "error",
        "code": "400",
        "data": None
    })

@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
def tests_me(request: HttpRequest):
    user = request.user
    tests_obj = Test.objects.filter(user__pk=user.pk).order_by("-id")
    tests = TestsModelSerializer(tests_obj, many=True)
    return Response(tests.data)


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
def test(request: HttpRequest, uuid: str):
    test_obj = Test.objects.filter(uuid=uuid)
    if not test_obj:
        return Response({
            "status": "error",
            "code": "404",
            "data": None
        })
    test_obj = test_obj.first()
    test = TestModelSerializer(test_obj, many=False)
    return Response(test.data)


@decorators.api_view(http_method_names=["POST"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
def set_test_set_time(request: HttpRequest, uuid: str):
    now = datetime.now(timezone.utc)
    test_obj = Test.objects.filter(uuid=uuid)
    if not test_obj:
        return Response({
            "status": "error",
            "code": "404",
            "data": None
        })
    test_obj = test_obj.first()
    test_obj.status = "started"
    test_obj.save()
    if not test_obj.start_time:
        test_obj.start_time = now
        test_obj.save()
    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })


@decorators.api_view(http_method_names=["POST"])
def submit(request: HttpRequest, uuid: str):
    now = datetime.now(tz=timezone.utc)
    test_obj = Test.objects.filter(uuid=uuid)
    if not test_obj:
        return Response({
            "status": "error",
            "code": "404",
            "data": None
        })
    test_obj = test_obj.first()
    questions = test_obj.questions.all()
    answer_keys = request.data.get("answers").split(",")
    if test_obj.questions.count() != len(answer_keys):
        return Response({
            "status": "error",
            "code": "400",
            "data": None
        })
    cases = {}
    counter = 1
    percentage = 0
    for question, answer in zip(questions, answer_keys):
        if answer == question.correct_answer:
            cases[f"{counter}"] = {
                "correct": question.correct_answer,
                "answer": answer,
                "status": True
            }
            percentage += question.score
        else:
            cases[f"{counter}"] = cases[f"{counter}"] = {
                "correct": question.correct_answer,
                "answer": answer,
                "status": False
            }
        counter+= 1
    print(percentage)
    print(test_obj.passed_score, percentage)
    if (test_obj.passed_score <= percentage):
        test_obj.status = "passed"
        test_obj.save()
    else:
        test_obj.status = "failed"
    if (test_obj.start_time):
        print(test_obj.start_time)
        print(now)
        print(now - test_obj.start_time)
        test_obj.elapsed = (now - test_obj.start_time).total_seconds()
    test_obj.percentage = percentage
    test_obj.cases = cases
    test_obj.save()
    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })


@decorators.api_view(http_method_names=["POST"])
def bulk_create(request: HttpRequest):
    raw_questions = request.data.get("raw")
    set_pk = request.data.get("set")
    set = Set.objects.get(pk=set_pk)
    for raw_q in raw_questions.split("\n\n"):
        q = raw_q.split("\n")
        content = q[0]
        a = q[1]
        b = q[2]
        c = q[3]
        d = q[4]
        answers = {
            "a": a,
            "b": b,
            "c": c,
            "d": d,
        }
        items = list(answers.items())
        random.shuffle(items)
        shuffled_answers = dict(items)
        print(shuffled_answers)
        question = Question.objects.create(
            question=content,
            set=set
        )
        ans_counter = 0
        akeys = "abcd"
        for ans in shuffled_answers:
            if ans == "a":
                question.correct_answer = akeys[ans_counter] 
            ans_counter += 1
        question.answer_a = list(shuffled_answers.values())[0]
        question.answer_b = list(shuffled_answers.values())[1]
        question.answer_c = list(shuffled_answers.values())[2]
        question.answer_d = list(shuffled_answers.values())[3]
        question.save()
    return Response()

@decorators.api_view(http_method_names=["GET"])
def print_test_as_pdf(request: HttpRequest, uuid: str):
    test_obj = Test.objects.filter(uuid=uuid)
    if not test_obj:
        return Response({
            "status": "error",
            "code": "404",
            "data": None
        })
    test_obj = test_obj.first()
    th = tuple(["Savol", "To'g'ri javob", "Javob", "Holati"])
    td = []
    pdf = PDF(orientation="landscape")
    for i in test_obj.cases:
        case = test_obj.cases[i]
        td += [(str(i), case.get("correct"), case.get("answer"), "To'g'ri" if case.get('status') else "Noto'g'ri")]
    TABLE = [th] + td

    questions = test_obj.questions.all()
    questions_html = ""
    for question in questions:
        questions_html += f"""
<li>
    {cyrillic_to_latin(question.question)}
    <ol>
        <li>{cyrillic_to_latin(question.answer_a)}</li>
        <li>{cyrillic_to_latin(question.answer_b)}</li>
        <li>{cyrillic_to_latin(question.answer_c)}</li>
        <li>{cyrillic_to_latin(question.answer_d)}</li>
    </ol>
</li>
"""

    questions_html = f"<ol>{questions_html}</ol>"
    pdf.add_page()
    pdf.set_font("Times", size=16)
    pdf.write_html(questions_html)
    pdf.add_page()
    with pdf.table(col_widths=[5, 25, 25, 35]) as table:
        for i, data_row in enumerate(TABLE):
            row = table.row()
            for j, datum in enumerate(data_row):
                row.cell(datum)
    response = HttpResponse(content=bytes(pdf.output()), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename=results.pdf'
    return response


@decorators.api_view(http_method_names=["GET"])
def print_tests_as_pdf(request: HttpRequest):
    tests_obj = Test.objects.exclude(status="not_started")
    tests_obj = tests_obj.exclude(status="started").order_by("-percentage")
    if not tests_obj:
        return Response({
            "status": "error",
            "code": "404",
            "data": None
        })
    th = tuple(["Nomi", "Ism Familiya", "Filial", "Bo'lim", "Lavozimi", "Natija %", "Holati"])
    td = []
    pdf = PDF(orientation="landscape")
    counter = 1
    for test in tests_obj:
        status = ""
        if test.status == "not_started":
            status = "Boshlanmagan"
        elif test.status == "passed":
            status = "O'tgan"
        elif test.status == "failed":
            status = "Yiqilgan"
        td += [(f"{counter}", f"{cyrillic_to_latin(test.user.first_name)} {cyrillic_to_latin(test.user.last_name)}", cyrillic_to_latin(test.user.branch), cyrillic_to_latin(test.user.department), cyrillic_to_latin(test.user.position), f"{test.percentage}",  status, )]
        counter += 1
    TABLE = [th] + td
    print(TABLE)
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(col_widths=[5, 15, 30, 20, 10, 5, 5]) as table:
        for i, data_row in enumerate(TABLE):
            row = table.row()
            for j, datum in enumerate(data_row):
                row.cell(datum)
    response = HttpResponse(content=bytes(pdf.output()), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename=results.pdf'
    return response


@decorators.api_view(http_method_names=["GET"])
def print_users_as_pdf(request: HttpRequest):
    users_obj = User.objects.filter(role="user")
    th = tuple(["ID", "Login", "Parol"])
    td = []
    pdf = PDF(orientation="landscape")
    counter = 1
    for user in users_obj:
        td += [(f"{counter}", f"{cyrillic_to_latin(user.username)}", "********" )]
        counter += 1
    TABLE = [th] + td
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table() as table:
        for i, data_row in enumerate(TABLE):
            row = table.row()
            for j, datum in enumerate(data_row):
                row.cell(datum)
    response = HttpResponse(content=bytes(pdf.output()), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename=users.pdf'
    return response


@decorators.api_view(http_method_names=["POST"])
def post_fine(request: HttpRequest):
    test_uuid = request.data.get("test")
    type = request.data.get("type")
    test_obj = Test.objects.get(uuid=test_uuid)
    if (type == "left"):
        test_obj.left = test_obj.left + 1
    elif (type == "right"):
        test_obj.right = test_obj.right + 1
    elif (type == "no_person"):
        test_obj.no_person = test_obj.no_person + 1
    elif (type == "two_person"):
        test_obj.two_person = test_obj.two_person + 1
    test_obj.save()
    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })

@decorators.api_view(http_method_names=["POST"])
def on_blur(request: HttpRequest):
    test_uuid = request.data.get("test")
    test_obj = Test.objects.get(uuid=test_uuid)
    test_obj.status = "ended"
    test_obj.percentage = 0
    test_obj.save()
    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })
