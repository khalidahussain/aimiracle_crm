from django.db import models
from clients.models import Client
from users.models import User

class TrainingSession(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.CharField(max_length=255)
    session_date = models.DateField()
    students_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='scheduled')

    def __str__(self):
        return f"{self.client.school_name} - {self.topic}"