from django.db import models
from django.contrib.auth.models import User

class Choices(models.Model):
    choice = models.CharField(max_length=5000)
    is_answer = models.BooleanField(default=False)
    
    def __str__(self):
        return self.choice_text

class Questions(models.Model):
    question = models.CharField(max_length= 10000)
    question_type = models.CharField(max_length=20)
    required = models.BooleanField(default= False)
    choices = models.ManyToManyField(Choices, related_name = "choices")

class Form(models.Model):
    STATUS_CHOICES = [
        ('edit', 'Edit'),
        ('publish', 'Publish'),
        ('republish', 'Republish'),
        ('close', 'Close'),
    ]
    code = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=10000, blank = True)
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "creator")
    collect_email = models.BooleanField(default=False)
    authenticated_responder = models.BooleanField(default = False)
    edit_after_submit = models.BooleanField(default=False)
    confirmation_message = models.CharField(max_length = 10000, default = "Your response has been recorded.")
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    questions = models.ManyToManyField(Questions, related_name = "questions")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Edit")