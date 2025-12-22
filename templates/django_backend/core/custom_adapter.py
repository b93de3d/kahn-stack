from allauth.account.adapter import DefaultAccountAdapter
from allauth.headless.adapter import DefaultHeadlessAdapter
import django.contrib.auth.models as auth_models
import core.serializers as core_serializers


class CustomAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return False


class CustomHeadlessAdapter(DefaultHeadlessAdapter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def serialize_user(self, user: auth_models.User):
        return core_serializers.User(instance=user).data
