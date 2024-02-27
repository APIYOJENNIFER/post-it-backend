"""Register the Group model to see it in Django admin"""
from django.contrib import admin
from .models import Group, Message

admin.site.register(Group)
admin.site.register(Message)
