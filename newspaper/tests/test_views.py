from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from newspaper.models import Topic, Redactor, Newspaper


TOPIC_URL = reverse("newspaper:topic-list")
REDACTOR_URL = reverse("newspaper:redactor-list")
NEWSPAPER_URL = reverse("newspaper:newspaper-list")


class PublicTopicTest(TestCase):
    def test_login_required(self):
        resp = self.client.get(TOPIC_URL)
        self.assertNotEqual(resp.status_code, 200)


class PrivetTopicTest(TestCase):
    def setUp(self) -> None:
        self.redactor = get_user_model().objects.create_user(
            username="redactor",
            password="redact555"
        )
        self.client.force_login(self.redactor)
        self.topic = Topic.objects.create(name="Old Topic")

    def test_retrieve_topic_list(self):
        Topic.objects.create(name="topic_1")
        Topic.objects.create(name="topic_2")
        resp = self.client.get(TOPIC_URL)
        self.assertEqual(resp.status_code, 200)
        topics = Topic.objects.all()
        self.assertEqual(
            list(resp.context["topic_list"]),
            list(topics)
        )
        self.assertTemplateUsed(resp, "newspaper/topic_list.html")

    def test_create_topic(self):
        response = self.client.post(reverse("newspaper:topic-create"), {"name": "New Topic"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Topic.objects.filter(name="New Topic").exists())

    def test_update_topic(self):
        response = self.client.post(
            reverse("newspaper:topic-update", args=[self.topic.id]),
            {"name": "Updated Topic"}
        )
        self.assertEqual(response.status_code, 302)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.name, "Updated Topic")

    def test_delete_topic(self):
        self.topic = Topic.objects.create(name="Topic to delete")
        response = self.client.post(
            reverse("newspaper:topic-delete", args=[self.topic.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Topic.objects.filter(name="Topic to delete").exists())


class PublicRedactorTest(TestCase):
    def test_login_required(self):
        resp = self.client.get(REDACTOR_URL)
        self.assertNotEqual(resp.status_code, 200)


class PrivetRedactorTest(TestCase):
    def setUp(self) -> None:
        self.redactor_1 = Redactor.objects.create(
            username="redactor1",
            password="redact123",
        )
        self.redactor_2 = Redactor.objects.create(
            username="redactor2",
            password="redact456"
        )
        self.client.force_login(self.redactor_1)

    def test_retrieve_redactor_list(self):
        resp = self.client.get(REDACTOR_URL)
        self.assertEqual(resp.status_code, 200)
        redactors = Redactor.objects.all()
        self.assertEqual(
            list(resp.context["redactor_list"]),
            list(redactors)
        )
        self.assertTemplateUsed(resp, "newspaper/redactor_list.html")

    def test_create_redactor(self):
        form_data = {
            "username": "new_redactor",
            "password1": "pas4268word",
            "password2": "pas4268word",
            "first_name": "John",
            "last_name": "Doe",
            "years_of_experience": 4
        }

        response = self.client.post(reverse("newspaper:redactor-create"), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Redactor.objects.filter(username="new_redactor").exists())

    def test_update_redactor_info(self):
        form_data = {"username": "redactor1"}
        response = self.client.post(reverse("newspaper:redactor-update", args=[self.redactor_1.id]), form_data)
        self.assertEqual(response.status_code, 302)
        self.redactor_1.refresh_from_db()
        self.assertEqual(self.redactor_1.username, "redactor1")

    def test_redactor_detail_view(self):
        response = self.client.get(reverse("newspaper:redactor-detail", args=[self.redactor_1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.redactor_1.username)
        self.assertTemplateUsed(response, "newspaper/redactor_detail.html")

    def test_delete_redactor(self):
        response = self.client.post(
            reverse("newspaper:redactor-delete", args=[self.redactor_1.id])
        )
        print(self.redactor_1.id)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Redactor.objects.filter(username="redactor1").exists())


class PublicNewspaperTest(TestCase):
    def test_login_required(self):
        resp = self.client.get(NEWSPAPER_URL)
        self.assertNotEqual(resp.status_code, 200)


class PrivetNewspaperTest(TestCase):
    def setUp(self) -> None:
        self.topic = Topic.objects.create(
            name="topictest"
        )
        self.redactor = get_user_model().objects.create_user(
            username="redactor",
            password="redactor888"
        )
        self.client.force_login(self.redactor)

    def test_retrieve_newspaper_list(self):
        newspaper = Newspaper.objects.create(
            title="news",
            topic=self.topic,
            content="test news"
        )
        newspaper.redactors.add(self.redactor)
        newspaper_1 = Newspaper.objects.create(
            title="newspaper",
            topic=self.topic,
            content="test newspaper"
        )
        newspaper_1.redactors.add(self.redactor)
        resp = self.client.get(NEWSPAPER_URL)
        self.assertEqual(resp.status_code, 200)
        newspapers = Newspaper.objects.all()
        self.assertEqual(
            list(resp.context["newspaper_list"]),
            list(newspapers)
        )
        self.assertTemplateUsed(resp, "newspaper/newspaper_list.html")

    def test_create_newspaper(self):
        form_data = {
            "title": "New Test Newspaper",
            "topic": self.topic.id,
            "content": "Test content for the newspaper",
            "redactors": self.redactor.id
        }
        response = self.client.post(reverse("newspaper:newspaper-create"), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Newspaper.objects.filter(title="New Test Newspaper").exists())

    def test_update_newspaper(self):
        newspaper = Newspaper.objects.create(
            title="Initial Title",
            topic=self.topic,
            content="Initial content"
        )
        form_data = {
            "title": "Updated Title",
            "topic": self.topic.id,
            "content": "Updated content",
            "redactors": self.redactor.id
        }
        response = self.client.post(
            reverse("newspaper:newspaper-update", args=[newspaper.id]),
            form_data
        )
        self.assertEqual(response.status_code, 302)
        newspaper.refresh_from_db()
        self.assertEqual(newspaper.title, "Updated Title")
        self.assertEqual(newspaper.content, "Updated content")

    def test_delete_newspaper(self):
        newspaper = Newspaper.objects.create(
            title="To be deleted",
            topic=self.topic,
            content="Content to be deleted"
        )
        response = self.client.post(reverse("newspaper:newspaper-delete", args=[newspaper.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Newspaper.objects.filter(id=newspaper.id).exists())
