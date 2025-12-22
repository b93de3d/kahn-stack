from typing import Type, Union, TypeVar
from allauth.account.forms import ResetPasswordForm


Model = TypeVar("Model")


def get_or_none(model: Type[Model], **kwargs) -> Union[Model, None]:
    """
    Object from Model.objects.get(**kwargs) or None
    """
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        obj = None
        # raise ValidationError({"error": [f"object not found: {model} {kwargs}"]})
    return obj


def send_password_reset_email(user):
    reset_form = ResetPasswordForm(data={"email": user.email})
    if reset_form.is_valid():
        reset_form.save(request=None)
