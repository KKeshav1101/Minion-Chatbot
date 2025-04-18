from django.db import models

# Create your models here.

class Conversation(models.Model):
    user_prompt=models.CharField(max_length=100000000000)
    response=models.CharField(max_length=100000000000)

