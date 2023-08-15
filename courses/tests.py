from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        """Инициализация"""
        self.user = User.objects.create(email="test@test.ru", password="12345", is_active=True, is_superuser=True)
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.lesson_test = Lesson.objects.create(
            name="Урок 1",
            description="Описание Урока №1",
        )

    def test_create_lesson(self):
        """Тест создания урока"""
        data = {
            "name": "test",
            "description": "Тестовый урок",
            "ref": "youtube.com/656655465",
        }

        response = self.client.post("/lessons/create/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.all().exists())

    def test_list_lesson(self):
        """Тест вывода всех уроков"""
        response = self.client.get("/lessons/")
        # print(response.json())

        data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "name": self.lesson_test.name,
                    "description": self.lesson_test.description,
                    "image": None,
                    "ref": None,
                    "amount_of_lessons": 1,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)

    def test_detail_lesson(self):
        """Вывод информации об одном уроке"""
        response = self.client.get(f"/lessons/{self.lesson_test.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        """Тест обновления урока"""
        data = {
            "name": "Обновленный урок 1",
            "description": "Обновленное описание тестового урока",
        }

        response = self.client.put(f"/lessons/update/{self.lesson_test.id}/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        """Тест удаления урока"""
        response = self.client.delete(f"/lessons/delete/{self.lesson_test.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
