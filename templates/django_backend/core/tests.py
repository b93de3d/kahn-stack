from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
import core.models as core_models


class AccountTests(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.staff_password = "LOLGG33$$$"
        staff_user = User.objects.create(
            username="staff", is_staff=True, is_superuser=True
        )
        staff_user.set_password(self.staff_password)
        staff_user.save()
        token = Token.objects.create(user=staff_user)
        self.staff_user = staff_user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    def test_create_customer(self):
        url = reverse("customers-list")
        print(url)
        data = {"name": "Rowan", "currency": "EUR"}
        response = self.client.post(url, data, format="json")
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(core_models.Customer.objects.count(), 1)
        self.assertEqual(core_models.Customer.objects.get().name, "Rowan")
