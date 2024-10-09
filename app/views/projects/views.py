from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from app.models import Project


class ProjectCreateView(CreateView):
    model = Project
    template_name = "projects/edit.html"
    fields = ["name", "set", "start_date", "end_date", "city"]
    success_url = "/projects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create Project"
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/detail.html"
    context_object_name = "project"

    def get_object(self):
        return Project.objects.get(id=self.kwargs["project_id"])


class ProjectListView(ListView):
    model = Project
    template_name = "projects/list.html"
    context_object_name = "projects"


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = "projects/edit.html"
    fields = ["name", "set", "start_date", "end_date", "city"]
    success_url = "/projects"

    def get_object(self):
        return Project.objects.get(id=self.kwargs["project_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Project"
        return context
