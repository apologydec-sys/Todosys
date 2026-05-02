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
    last_reminded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.content

    def needs_reminder(self):
        """Return True if this task needs a reminder (incomplete and 6+ mins since last reminder)."""
        if self.complete:
            return False
        if self.last_reminded_at is None:
            return True
        elapsed = timezone.now() - self.last_reminded_at
        return elapsed.total_seconds() >= 360  # 6 minutes