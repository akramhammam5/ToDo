from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Link to the User model
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ], default='Pending')
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp for task creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for task updates

    def __str__(self):
        return self.name
