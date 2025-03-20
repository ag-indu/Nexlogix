from django.db import models
from django.contrib.auth.models import User

class Business(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, null=True, blank=True)  # Allow null values
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
