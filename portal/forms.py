from django import forms
from .models import AcademicGroup, Course, Department


class PortalModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-select" if isinstance(field.widget, forms.Select) else "form-control"


class CourseForm(PortalModelForm):
    class Meta:
        model = Course
        fields = ["title", "department", "teacher", "hours"]


class DepartmentForm(PortalModelForm):
    class Meta:
        model = Department
        fields = ["title", "code"]


class AcademicGroupForm(PortalModelForm):
    class Meta:
        model = AcademicGroup
        fields = ["title", "department", "year"]
