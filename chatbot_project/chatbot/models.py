from django.db import models

# Create your models here.
class Conversation(models.Model):
    user_id = models.CharField(max_length=255)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    