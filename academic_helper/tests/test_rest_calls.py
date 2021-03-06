from django.test import Client
from django.test import TestCase, RequestFactory
import json
import io
from ics import Calendar
from academic_helper.management import init_data
from academic_helper.management.init_data import create_all
from academic_helper.views.schedule import ScheduleView
from academic_helper.models import CoursistUser

urls_to_get = [
    "",
    "/ajax/",
    "/courses/",
    "/courses/" + str(init_data.courses_to_fetch[0]),
    "/about/",
    "/schedule/",
    "/user/admin/",
    "/degree-program",
    "/health_check/",
    "/accounts/signup/",
    "/accounts/login/",
]


class TestRestCalls(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CoursistUser.objects.create_user(
            username="test_user", email="test_user@test_user.com", password="nuclear"
        )

    @classmethod
    def setUpTestData(cls):
        create_all()

    def test_get_urls(self):
        client = Client()
        for url in urls_to_get:
            response = client.get(url, follow=True)
            self.assertEquals(response.status_code, 200)

    def test_get_schedule_export_empty(self):

        request = self.factory.get("/schedule", {"download": "json"})
        request.user = self.user
        response = ScheduleView.as_view()(request)

        self.assertEquals(response.status_code, 200)
        self.assertIn("attachment; filename=", response.get("Content-Disposition"))
        self.assertEqual(response["content-type"], "application/json")

        result_bytes = b"".join(response.streaming_content)
        result = json.loads(result_bytes)
        self.assertEquals(result, json.loads(b"[]"))

    def test_get_schedule_export_empty_ical(self):

        request = self.factory.get("/schedule", {"download": "ical"})
        request.user = self.user
        response = ScheduleView.as_view()(request)

        self.assertEquals(response.status_code, 200)
        self.assertIn("attachment; filename=", response.get("Content-Disposition"))
        self.assertEqual(response["content-type"], "text/calendar")

        result_bytes = b"".join(response.streaming_content)
        expected_result = io.BytesIO()
        expected_result.writelines([line.encode() for line in Calendar()])
        expected_result.seek(0)
        self.assertEquals(result_bytes, expected_result.read())

    def test_post_urls(self):
        pass
