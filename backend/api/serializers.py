from rest_framework import serializers
from todo.models import Todo
from rest_framework import generics

from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




class TodoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()
    class Meta:
        model = Todo
        fields = ['id','title','memo','created','completed']

class TodoToggleCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id'] # why need to show id?
        read_only_fields = ['title','memo','created','completed']