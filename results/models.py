from django.db import models
from django.contrib.auth.models import User
from create_form.models import Form
from answers.models import Answer

# Create your models here.
class Responses(models.Model):
    response_code = models.CharField(max_length=20)
    response_to = models.ForeignKey(Form, on_delete = models.CASCADE, related_name = "response_to")
    responder_ip = models.CharField(max_length=30)
    responder = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "responder", blank = True, null = True)
    responder_email = models.EmailField(blank = True, null= True)
    response = models.ManyToManyField(Answer, related_name = "response")