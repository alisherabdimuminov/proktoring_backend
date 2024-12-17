from uuid import uuid4
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from users.models import User


ANSWER = (
    ("a", "A"),
    ("b", "B"),
    ("c", "C"),
    ("d", "D"),
)
STATUS = (
    ("not_started", "Boshlanmagan"),
    ("started", "Boshlangan"),
    ("passed", "O'tgan"),
    ("failed", "Yiqilgan"),
    ("ended", "Tugagan"),
)

def json():
    return {}


class Set(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    question = models.TextField()
    answer_a = models.TextField()
    answer_b = models.TextField()
    answer_c = models.TextField()
    answer_d = models.TextField()
    correct_answer = models.CharField(max_length=1, choices=ANSWER)
    score = models.IntegerField(default=2)

    def __str__(self):
        return self.question
    
class Test(models.Model):
    uuid = models.CharField(max_length=100, default=uuid4)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    passed_score = models.IntegerField()
    questions_count = models.IntegerField(default=120)
    start_time = models.DateTimeField(null=True, blank=True)
    questions = models.ManyToManyField(Question, related_name="test_questions", null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS, default="not_started", null=True, blank=True)
    percentage = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True, blank=True)
    elapsed = models.IntegerField(default=0, null=True, blank=True)
    cases = models.JSONField(default=json, null=True, blank=True)
    
    right = models.IntegerField(default=0, null=True, blank=True)
    left = models.IntegerField(default=0, null=True, blank=True)
    two_person = models.IntegerField(default=0, null=True, blank=True)
    no_person = models.IntegerField(default=0, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def count_q(self):
        return self.questions.count()
