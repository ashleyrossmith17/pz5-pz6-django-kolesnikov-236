from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile, name="profile"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("<str:kind>/", views.entity_list, name="entity_list"),
    path("<str:kind>/add/", views.object_form, name="object_add"),
    path("<str:kind>/<int:pk>/edit/", views.object_form, name="object_edit"),
    path("<str:kind>/<int:pk>/delete/", views.object_delete, name="object_delete"),
]
