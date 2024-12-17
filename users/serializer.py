from rest_framework import serializers

from .models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "uuid", "username", "first_name", "last_name", "middle_name", "role", "role", "pwd", )
