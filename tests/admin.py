from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Set, Question, Test


@admin.register(Set)
class SetModelAdmin(ModelAdmin):
    list_display = ["name"]


@admin.register(Question)
class QuestionModelAdmin(ModelAdmin):
    list_display = ["question", "set", "correct_answer", ]


@admin.register(Test)
class TestModelAdmin(ModelAdmin):
    list_display = ["name", "user", "set", "count_q", ]
