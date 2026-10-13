from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Department(models.Model):
    title = models.CharField("Название факультета", max_length=160, unique=True)
    code = models.CharField("Код", max_length=12, unique=True)

    class Meta:
        ordering = ["code"]
        verbose_name = "Факультет"
        verbose_name_plural = "Факультеты"

    def __str__(self):
        return f"{self.code} · {self.title}"


class AcademicGroup(models.Model):
    title = models.CharField("Учебная группа", max_length=40, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="academic_groups", verbose_name="Факультет")
    year = models.PositiveSmallIntegerField("Курс обучения", default=2, validators=[MinValueValidator(1), MaxValueValidator(6)])

    class Meta:
        ordering = ["title"]
        verbose_name = "Учебная группа"
        verbose_name_plural = "Учебные группы"

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField("Название курса", max_length=180)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="courses", verbose_name="Факультет")
    teacher = models.CharField("Преподаватель", max_length=120)
    hours = models.PositiveIntegerField("Часы", default=72, validators=[MinValueValidator(1), MaxValueValidator(1000)])

    class Meta:
        ordering = ["title"]
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Profile(models.Model):
    STUDENT, METHODIST, ADMIN = "student", "methodist", "admin"
    ROLES = [(STUDENT, "Студент"), (METHODIST, "Методист"), (ADMIN, "Администратор")]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField("Роль", max_length=20, choices=ROLES, default=STUDENT)
    academic_group = models.ForeignKey(AcademicGroup, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Группа")

    def __str__(self):
        return self.user.get_username()
