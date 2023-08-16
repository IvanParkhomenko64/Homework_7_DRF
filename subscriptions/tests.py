from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson
from subscriptions.models import Subscription
from users.models import User


class SubscriptionTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='admin@test.ru',
        )
        self.user.set_password('12345')
        self.user.save()

        self.course = Course.objects.create(
            name='тестовый курс',
            description='описание тестового курса',
        )

        self.lesson = Lesson.objects.create(
            name='test',
            description='test description',
            ref='youtube.com/526565',
            owner=self.user,
            course=self.course,
        )

    def test_subscription_create(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'course': self.course.pk,
            'subscriber': self.user.pk,
        }

        response = self.client.post(
            path='/subscriptions/create/', data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('course'), self.course.pk)
        self.assertEqual(response.json().get('subscriber'), self.user.pk)

    def test_subscription_delete(self):
        subscription = Subscription.objects.create(
            course=self.course,
            subscriber=self.user,
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            f'/subscriptions/delete/{subscription.pk}/',
        )

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Subscription.objects.all().exists(),
        )
