from django.contrib import admin
# from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = ["username", "first_name", "last_name", "middle_name", "role", ]
    search_fields = ["username", ]

    add_form = UserCreationForm
    form = UserChangeForm

    add_fieldsets = (
        ("Xodim qo'shish", {
            "fields": ("username", "password1", "password2", "first_name", "last_name", "middle_name", "phone", "branch", "department", "position", "role", "pwd")
        }),
    )
    fieldsets = (
        ("Xodimni tahrirlash", {
            "fields": ("username", "first_name", "last_name", "middle_name", "phone", "branch", "department", "position", "role", "pwd")
        }),
    )

