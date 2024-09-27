from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls.base import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="admintest123",
        )
        self.client.force_login(self.admin)
        self.redactor = get_user_model().objects.create_user(
            username="redactor",
            password="test987",
            years_of_experience=10
        )

    def test_redactor_experience_listed(self) -> None:
        url = reverse("admin:newspaper_redactor_changelist")
        resp = self.client.get(url)
        self.assertContains(resp, self.redactor.years_of_experience)

    def test_redactor_experience_listed_on_redactor_detail_page(self) -> None:
        url = reverse("admin:newspaper_redactor_change", args=[self.redactor.id])
        resp = self.client.get(url)
        self.assertContains(resp, self.redactor.years_of_experience)

    def test_redactor_experience_add_to_driver_create_page(self) -> None:
        url = reverse("admin:newspaper_redactor_add")
        resp = self.client.get(url)
        self.assertContains(resp, "years_of_experience")
