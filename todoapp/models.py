from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.content