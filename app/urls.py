"""
URL configuration for projectr `app`.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from app.views import views
from app.views.projects import views as project_views

urlpatterns = [
    path("", name="index", view=views.index),
    path("accounts/profile/", name="profile", view=views.profile),
    path(
        "projects/", name="projects_list", view=project_views.ProjectListView.as_view()
    ),
    path(
        "projects/calculate/",
        name="projects_calculate",
        view=project_views.ProjectCalculateReimbursementsView.as_view(),
    ),
    path(
        "projects/create/",
        name="projects_create",
        view=project_views.ProjectCreateView.as_view(),
    ),
    path(
        "projects/<int:project_id>/",
        name="projects_detail",
        view=project_views.ProjectDetailView.as_view(),
    ),
    path(
        "projects/<int:project_id>/edit/",
        name="projects_edit",
        view=project_views.ProjectUpdateView.as_view(),
    ),
]
