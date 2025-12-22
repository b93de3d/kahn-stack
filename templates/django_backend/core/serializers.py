from django.db import transaction
from rest_framework import serializers
import django.contrib.auth.models as auth_models
from rest_framework.exceptions import ValidationError
import core.models as core_models
from tools.dynamic_rest.fields import DynamicRelationField
from tools.dynamic_rest.serializers import DynamicSerializer

from tools.util import send_password_reset_email


class UserProfile(DynamicSerializer):
    uuid = serializers.UUIDField()
    avatar = serializers.FileField(allow_null=True)

    class Meta:
        model = core_models.UserProfile


class UpdateUserProfile(DynamicSerializer):
    avatar = serializers.FileField(allow_null=True)

    class Meta:
        model = core_models.UserProfile


class User(DynamicSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
    has_usable_password = serializers.BooleanField()
    profile = DynamicRelationField(UserProfile, many=False, embed=True, link=False)

    class Meta:
        model = auth_models.User


class CreateUser(DynamicSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_superuser = serializers.BooleanField()

    def validate_email(self, email):
        if auth_models.User.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def create(self, validated_data):
        with transaction.atomic():
            validated_data["username"] = validated_data["email"]
            validated_data["is_staff"] = True
            user = super().create(validated_data)
            send_password_reset_email(user)
            core_models.UserProfile.objects.create(user=user)
        return user

    class Meta:
        model = auth_models.User


class UpdateUser(DynamicSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_superuser = serializers.BooleanField()

    class Meta:
        model = auth_models.User


class ExampleUser(DynamicSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = auth_models.User


class Example(DynamicSerializer):

    uuid = serializers.UUIDField()
    title = serializers.CharField()
    example_type = serializers.ChoiceField(choices=core_models.Example.Type.choices)
    likes = serializers.IntegerField()
    is_good_example = serializers.BooleanField()
    created = serializers.DateTimeField()
    created_by = DynamicRelationField(ExampleUser, many=False, embed=True)

    class Meta:
        model = core_models.Example
