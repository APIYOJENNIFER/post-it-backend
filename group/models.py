"""Models module"""
from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    """Group class model"""
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(User, related_name='groups_joined')
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='groups_created')

    def __str__(self) -> str:
        return str(self.name)


class Message(models.Model):
    """A model to define the structure of messages"""
    post = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='messages_authored')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.post}'
