from django.contrib import admin
from .models import AcademicGroup, Course, Department, Profile

admin.site.register([AcademicGroup, Course, Department, Profile])
