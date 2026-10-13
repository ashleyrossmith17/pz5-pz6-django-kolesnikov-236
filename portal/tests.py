from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import AcademicGroup, Course, Department, Profile


class PortalTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(title="Информатика", code="И3")
        self.other = Department.objects.create(title="Авиация", code="И1")
        self.group = AcademicGroup.objects.create(title="М3О-236БВ-25", department=self.department)
        self.course = Course.objects.create(title="Базы данных", department=self.department, teacher="Манин А. Н.", hours=72)
        Course.objects.create(title="Графика", department=self.other, teacher="Иванов И. И.", hours=36)
        self.manager = get_user_model().objects.create_user("manager", password="test-only-password")
        Profile.objects.create(user=self.manager, role=Profile.METHODIST, academic_group=self.group)
        self.student = get_user_model().objects.create_user("student", password="test-only-password")
        Profile.objects.create(user=self.student, academic_group=self.group)

    def test_anonymous_redirect(self):
        self.assertEqual(self.client.get("/courses/").status_code, 302)

    def test_manager_pages_and_mode(self):
        self.client.force_login(self.manager)
        for url in ["/", "/courses/", "/departments/", "/groups/", "/dashboard/", "/courses/add/"]:
            self.assertEqual(self.client.get(url).status_code, 200)
        self.client.get("/?ui=classic")
        self.assertContains(self.client.get("/courses/"), "mode-classic")

    def test_student_cannot_write(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get("/courses/add/").status_code, 403)
        self.assertEqual(self.client.post(f"/courses/{self.course.pk}/delete/").status_code, 403)
        self.assertTrue(Course.objects.filter(pk=self.course.pk).exists())

    def test_course_create_validation_edit_delete(self):
        self.client.force_login(self.manager)
        data = {"title": "Новый курс", "department": self.department.pk, "teacher": "Петров", "hours": 0}
        self.assertEqual(self.client.post("/courses/add/", data).status_code, 200)
        self.assertFalse(Course.objects.filter(title="Новый курс").exists())
        data["hours"] = 40
        self.assertEqual(self.client.post("/courses/add/", data).status_code, 302)
        course = Course.objects.get(title="Новый курс")
        data["hours"] = 80
        self.assertEqual(self.client.post(f"/courses/{course.pk}/edit/", data).status_code, 302)
        course.refresh_from_db()
        self.assertEqual(course.hours, 80)
        self.client.get(f"/courses/{course.pk}/delete/")
        self.assertTrue(Course.objects.filter(pk=course.pk).exists())
        self.assertEqual(self.client.post(f"/courses/{course.pk}/delete/").status_code, 302)

    def test_protected_department(self):
        self.client.force_login(self.manager)
        response = self.client.post(f"/departments/{self.department.pk}/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Сначала удалите")

    def test_dashboard_filter_and_invalid_parameter(self):
        self.client.force_login(self.manager)
        all_data = self.client.get("/dashboard/").context
        self.assertEqual(all_data["total_courses"], 2)
        selected = self.client.get(f"/dashboard/?department={self.department.pk}").context
        self.assertEqual(selected["total_courses"], 1)
        self.assertEqual(selected["total_users"], 2)
        self.assertEqual(selected["chart_data"]["courses"]["values"], [1])
        for parameter in ["garbage", "999999"]:
            self.assertEqual(self.client.get(f"/dashboard/?department={parameter}").context["total_courses"], 2)

    def test_dashboard_empty_and_json_escaping(self):
        self.client.force_login(self.manager)
        Department.objects.create(title="Пустой факультет", code="EMPTY")
        self.department.code = "</script>"
        self.department.save()
        response = self.client.get("/dashboard/")
        self.assertContains(response, r"\u003C/script\u003E")
        self.assertEqual(sum(response.context["chart_data"]["users"]["values"]), 2)

    def test_login_and_post_logout(self):
        self.assertEqual(self.client.post("/login/", {"username": "manager", "password": "test-only-password"}).status_code, 302)
        self.assertEqual(self.client.get("/logout/").status_code, 405)
        self.assertEqual(self.client.post("/logout/").status_code, 302)
