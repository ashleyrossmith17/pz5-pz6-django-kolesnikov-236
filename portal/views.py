from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.db.models.deletion import ProtectedError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AcademicGroupForm, CourseForm, DepartmentForm
from .models import AcademicGroup, Course, Department, Profile

ENTITIES = {
    "courses": (Course, CourseForm, "Курсы", "course_list.html"),
    "departments": (Department, DepartmentForm, "Факультеты", "department_list.html"),
    "groups": (AcademicGroup, AcademicGroupForm, "Учебные группы", "academic_group_list.html"),
}


def entity_config(kind):
    if kind not in ENTITIES:
        raise Http404
    return ENTITIES[kind]


def require_manager(user):
    profile = getattr(user, "profile", None)
    if not (user.is_staff or (profile and profile.role in (Profile.METHODIST, Profile.ADMIN))):
        raise PermissionDenied


@login_required
def profile(request):
    details, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, "profile.html", {"details": details})


@login_required
def entity_list(request, kind):
    model, _, title, template = entity_config(kind)
    objects = model.objects.all()
    if kind != "departments":
        objects = objects.select_related("department")
    return render(request, template, {"objects": objects, "page_title": title, "kind": kind})


@login_required
def object_form(request, kind, pk=None):
    require_manager(request.user)
    model, form_class, title, _ = entity_config(kind)
    instance = get_object_or_404(model, pk=pk) if pk else None
    form = form_class(request.POST if request.method == "POST" else None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Изменения сохранены.")
        return redirect("entity_list", kind=kind)
    return render(request, "object_form.html", {"form": form, "page_title": "Изменение записи" if pk else "Добавление записи", "kind": kind, "section_title": title})


@login_required
def object_delete(request, kind, pk):
    require_manager(request.user)
    model, _, title, _ = entity_config(kind)
    instance = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        try:
            instance.delete()
            messages.success(request, "Запись удалена.")
            return redirect("entity_list", kind=kind)
        except ProtectedError:
            messages.error(request, "Сначала удалите или перенесите связанные курсы и группы.")
    return render(request, "object_confirm_delete.html", {"object": instance, "kind": kind, "section_title": title})


@login_required
def dashboard(request):
    departments = Department.objects.all()
    selected_id = request.GET.get("department", "")
    selected = departments.filter(pk=selected_id).first() if selected_id.isdecimal() else None
    courses, groups = Course.objects.all(), AcademicGroup.objects.all()
    users = get_user_model().objects.filter(is_active=True)
    chart_departments = departments
    if selected:
        courses = courses.filter(department=selected)
        groups = groups.filter(department=selected)
        users = users.filter(profile__academic_group__department=selected)
        chart_departments = departments.filter(pk=selected.pk)
    course_counts = list(chart_departments.annotate(total=Count("courses")))
    group_counts = list(chart_departments.annotate(total=Count("academic_groups")))
    role_counts = dict(users.values("profile__role").annotate(total=Count("id")).values_list("profile__role", "total"))
    chart_data = {
        "courses": {"labels": [d.code for d in course_counts], "values": [d.total for d in course_counts]},
        "groups": {"labels": [d.code for d in group_counts], "values": [d.total for d in group_counts]},
        "users": {"labels": [label for _, label in Profile.ROLES] + ["Без профиля"], "values": [role_counts.get(role, 0) for role, _ in Profile.ROLES] + [role_counts.get(None, 0)]},
    }
    return render(request, "dashboard.html", {
        "departments": departments, "selected_department": str(selected.pk) if selected else "",
        "total_courses": courses.count(), "total_groups": groups.count(),
        "total_departments": 1 if selected else departments.count(), "total_users": users.count(),
        "chart_data": chart_data,
    })
