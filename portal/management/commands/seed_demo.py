import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from portal.models import AcademicGroup, Course, Department, Profile


class Command(BaseCommand):
    help = "Создать повторяемый набор учебных данных."

    @transaction.atomic
    def handle(self, *args, **options):
        password = os.environ.get("DEMO_PASSWORD")
        if not password:
            raise CommandError("Укажите DEMO_PASSWORD в окружении перед запуском.")
        departments = []
        for code, title in [("И3", "Системы управления, информатика и электроэнергетика"), ("И1", "Авиационная техника"), ("И6", "Аэрокосмические системы")]:
            department, _ = Department.objects.update_or_create(code=code, defaults={"title": title})
            departments.append(department)
        groups = []
        for title, department_index, year in [("М3О-236БВ-25", 0, 2), ("М3О-235БВ-25", 0, 2), ("М1О-201Б-25", 1, 2), ("М6О-101Б-26", 2, 1)]:
            group, _ = AcademicGroup.objects.update_or_create(title=title, defaults={"department": departments[department_index], "year": year})
            groups.append(group)
        for title, index, teacher, hours in [
            ("Структура программного обеспечения и базы данных", 0, "Манин А. Н.", 72),
            ("Веб-программирование", 0, "Соколов И. В.", 108),
            ("Алгоритмы и структуры данных", 0, "Иванова Е. А.", 144),
            ("Проектирование авиационных систем", 1, "Петров Д. С.", 108),
            ("Инженерная графика", 1, "Кузнецова О. М.", 72),
            ("Основы космической техники", 2, "Смирнов П. А.", 108),
        ]:
            Course.objects.update_or_create(title=title, defaults={"department": departments[index], "teacher": teacher, "hours": hours})
        for username, first, last, role, group_index in [
            ("kolesnikov", "Кирилл Петрович", "Колесников", Profile.METHODIST, 0),
            ("student1", "Алексей", "Орлов", Profile.STUDENT, 0),
            ("student2", "Мария", "Волкова", Profile.STUDENT, 1),
            ("student3", "Антон", "Белов", Profile.STUDENT, 2),
            ("student4", "Дарья", "Морозова", Profile.STUDENT, 3),
            ("administrator", "Иван", "Администратор", Profile.ADMIN, None),
        ]:
            user, created = get_user_model().objects.get_or_create(username=username)
            user.first_name, user.last_name = first, last
            user.is_staff = role == Profile.ADMIN
            if created:
                user.set_password(password)
            user.save()
            Profile.objects.update_or_create(user=user, defaults={"role": role, "academic_group": groups[group_index] if group_index is not None else None})
        self.stdout.write(self.style.SUCCESS("Данные готовы: 3 факультета, 4 группы, 6 курсов, 6 пользователей."))
