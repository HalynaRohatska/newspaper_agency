from django.contrib.auth import get_user_model
from django.test import TestCase

from newspaper.models import Topic, Newspaper


class ModelsTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            name="topic"
        )
        self.redactor = get_user_model().objects.create(
            username="user",
            password="redact123",
            first_name="Tom",
            last_name="Brain",
        )
        self.newspaper = Newspaper.objects.create(
            title="news",
            topic=self.topic,
            content="test str newspaper"
        )

    def test_topic_str(self) -> None:
        self.assertEqual(
            str(self.topic),
            f"{self.topic.name}"
        )

    def test_redactor_str(self) -> None:
        self.assertEqual(
            str(self.redactor),
            f"{self.redactor.username} "
            f"({self.redactor.first_name} {self.redactor.last_name})"
        )

    def test_newspaper_str(self) -> None:
        self.assertEqual(
            str(self.newspaper),
            f"{self.newspaper.title} ({self.newspaper.content})"
        )
