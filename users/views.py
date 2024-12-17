from django.http import HttpRequest
from rest_framework import decorators
from rest_framework import generics
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from utils.generate import generate

from .models import User
from .serializer import UserModelSerializer



class UsersListAPIView(generics.ListAPIView):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserModelSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ["branch"]


@decorators.api_view(http_method_names=["POST"])
def add_user(request: HttpRequest):
    username = request.data.get("username")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    middle_name = request.data.get("middle_name")
    phone = request.data.get("phone")
    branch = request.data.get("branch")
    department = request.data.get("department")
    position = request.data.get("position")
    password = request.data.get("password")
    try:
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            branch=branch,
            department=department,
            position=position,
            phone=phone,
            pwd=password,
            role="user"
        )
        user.set_password(password)
        user.save()
        return Response({
            "status": "success",
            "code": "201",
            "data": None
        })
    except:
        return Response({
            "status": "error",
            "code": "400",
            "data": None
        })


@decorators.api_view(http_method_names=["POST"])
def edit_user(request: HttpRequest, uuid: str):
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    middle_name = request.data.get("middle_name")
    phone = request.data.get("phone")
    branch = request.data.get("branch")
    department = request.data.get("department")
    position = request.data.get("position")
    password = request.data.get("password")
    user = User.objects.get(uuid=uuid)
    try:
        user.first_name = first_name
        user.last_name = last_name
        user.middle_name = middle_name
        user.phone = phone
        user.branch = branch
        user.department = department
        user.position = position
        user.pwd = password
        user.set_password(password)
        user.save()
        return Response({
            "status": "success",
            "code": "201",
            "data": None
        })
    except:
        return Response({
            "status": "error",
            "code": "400",
            "data": None
        })


@decorators.api_view(http_method_names=["POST"])
def login(request: HttpRequest):
    username = request.data.get("username")
    password = request.data.get("password")
    user = User.objects.filter(username=username)
    if not user:
        return Response({
            "status": "error",
            "code": "404",
            "data": None
        })
    user = user.first()
    if not user.check_password(password):
        return Response({
            "status": "error",
            "code": "400",
            "data": None
        })
    token = Token.objects.get_or_create(user=user)
    return Response({
        "status": "success",
        "code": "200",
        "data": {
            "uuid": user.uuid.__str__(),
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "middle_name": user.middle_name,
            "role": user.role,
            "pwd": user.pwd,
            "token": token[0].key
        }
    })
