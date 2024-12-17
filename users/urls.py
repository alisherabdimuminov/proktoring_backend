from django.urls import path

from .views import (
    UsersListAPIView,
    add_user,
    edit_user,

    login,
)
from tests.views import print_users_as_pdf


urlpatterns = [
    path("", UsersListAPIView.as_view(), name="users"),
    path("add/", add_user, name="add_user"),
    path("<str:uuid>/edit/", edit_user, name="edit_user"),
    path("login/", login, name="login"),
    path("pdf/", print_users_as_pdf, name="print_users"),
]
