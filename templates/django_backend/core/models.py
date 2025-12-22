from uuid import uuid4
from django.db import models
from django.db import transaction as db_transaction
import django.contrib.auth.models as auth_models
from django.db.models import F
from django.utils import timezone


class Example(models.Model):
    class Type(models.TextChoices):
        FOO = "FOO"
        BAR = "BAR"
        BAZ = "BAZ"

    uuid = models.UUIDField(default=uuid4, unique=True)
    title = models.CharField(max_length=100)
    example_type = models.CharField(max_length=25, choices=Type.choices)
    likes = models.IntegerField(default=0)
    is_good_example = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        auth_models.User, on_delete=models.CASCADE, related_name="examples"
    )


class UserProfile(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True)
    user = models.OneToOneField(
        auth_models.User, on_delete=models.CASCADE, related_name="profile"
    )
    avatar = models.FileField(null=True)
