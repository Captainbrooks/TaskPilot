from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

def future_date_validator(value):
    if value <= timezone.now().date():
        raise ValidationError("Deadline must be in the future.")

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    task_title = models.CharField(max_length=200)
    task_description = models.TextField(max_length=400)
    task_deadline = models.DateField(validators=[future_date_validator])
    
    def __str__(self):
        return self.task_title
