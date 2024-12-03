from django.contrib import admin

# Register your models here.
from .models import Choices, Questions, Form

admin.site.register(Choices)
admin.site.register(Questions)
admin.site.register(Form)
