from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=50, unique=True)
    password=models.CharField(max_length=128)
    email=models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return self.username