from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name=models.CharField(max_length=255, unique=True)
    members=models.ManyToManyField(User, related_name='groups_joined')
    creator=models.ForeignKey(User, on_delete=models.CASCADE, related_name='groups_created')

    def __str__(self):
        return self.name