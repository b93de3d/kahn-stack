from django.core.files.base import ContentFile
from django.db import transaction as db_transaction
from django.db.models import Prefetch, Q, F
from django.db.models.aggregates import Sum, Count
from rest_framework import permissions, mixins, status, serializers
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet
import django.contrib.auth.models as auth_models
import core.models as core_models
import core.serializers as core_serializers
from _KAHN_PROJECT_SLUG_.settings import GIT_VERSION
from tools.dynamic_rest.viewsets import (
    WithDynamicViewSetMixin,
    ViewSetReturnType,
    ViewSetReturnTypeItem,
    pagination_params,
)
from django.middleware.csrf import get_token as get_csrf_token


@api_view(["GET"])
@permission_classes([])
def csrf(request):
    token = get_csrf_token(request)
    return Response(data={"csrfToken": token}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([])
def version(request):
    return Response(data=GIT_VERSION, status=status.HTTP_200_OK)


class CreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                self.serializer_class.get_name(): self.serializer_class(
                    instance=instance
                ).data
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class PartialUpdateModelMixin:
    """
    Update a model instance.
    """

    def _update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(
            {
                self.serializer_class.get_name(): self.serializer_class(
                    instance=instance
                ).data
            }
        )

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        return self._update(request, *args, **kwargs)


class UserViewSet(
    WithDynamicViewSetMixin,
    CreateModelMixin,
    PartialUpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = core_serializers.User
    permission_classes = [
        permissions.IsAdminUser,
    ]
    lookup_field = "id"

    def get_queryset(self, queryset=None):
        return auth_models.User.objects.all()

    def get_serializer_class(self):
        return self.auto_get_serializer_class(core_serializers)


class UserProfileViewSet(
    WithDynamicViewSetMixin,
    PartialUpdateModelMixin,
    GenericViewSet,
):
    serializer_class = core_serializers.UserProfile
    permission_classes = [
        permissions.IsAdminUser,
    ]
    lookup_field = "uuid"

    def get_queryset(self, queryset=None):
        return core_models.UserProfile.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return self.auto_get_serializer_class(core_serializers)


class ExampleViewSet(
    WithDynamicViewSetMixin,
    CreateModelMixin,
    mixins.RetrieveModelMixin,
    PartialUpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = core_serializers.Example
    permission_classes = [
        permissions.IsAdminUser,
    ]
    lookup_field = "uuid"

    def get_queryset(self, queryset=None):
        return core_models.Example.objects.all()

    def get_serializer_class(self):
        return self.auto_get_serializer_class(core_serializers)
