from django.urls import path

from .views import (
    QuestionListAPIView,
    SetsListAPIView,
    TestsListAPIView,

    add_question,
    add_set,
    add_test,

    edit_question,
    edit_set,
    edit_test,

    tests_me,
    test,
    set_test_set_time,
    submit,
    bulk_create,
    print_test_as_pdf,
    print_tests_as_pdf,
    post_fine,
    on_blur,
)


urlpatterns = [
    path("questions/", QuestionListAPIView.as_view(), name="questions"),
    path("sets/", SetsListAPIView.as_view(), name="sets"),
    path("tests/", TestsListAPIView.as_view(), name="tests"),
    path("tests/pdf/", print_tests_as_pdf, name="tests_pdf"),
    
    path("questions/add/", add_question, name="add_question"),
    path("sets/add/", add_set, name="add_set"),
    path("tests/add/", add_test, name="add_test"),

    path("questions/<int:pk>/edit/", edit_question, name="edit_test"),
    path("sets/<int:pk>/edit/", edit_set, name="edit_set"),
    path("tests/<int:pk>/edit/", edit_test, name="edit_test"),

    path("tests/me/", tests_me, name="test_me"),
    path("tests/test/<str:uuid>/", test, name="test"),
    path("tests/test/<str:uuid>/pdf/", print_test_as_pdf, name="test_pdf"),
    path("tests/test/<str:uuid>/set_start_time/", set_test_set_time, name="set_start_time"),
    path("tests/test/<str:uuid>/submit/", submit, name="submit"),
    path("bulk/", bulk_create, name="bulk_create"),
    path("fine/", post_fine, name="fine"),
    path("blur/", on_blur, name="blur"),
]
