from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from app.models import Project


class ProjectCalculateReimbursementsView(View):
    def post(self, request, *args, **kwargs):
        redirect_target = reverse("projects_list")
        project_set = request.POST.get("project_set")

        if project_set:
            projects = Project.objects.filter(set=project_set)
            redirect_target = reverse("projects_list") + f"?project_set={project_set}"
        else:
            projects = Project.objects.all()

        project_sets = set([project.set for project in projects])
        for project_set in project_sets:
            total_reimbursement = Project.calculate_reimbursement_for_project_set(
                project_set
            )
            print(f"Set {project_set} reimbursement: ${total_reimbursement}")

        return redirect(redirect_target)


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

    def get_queryset(self):
        queryset = super().get_queryset()
        project_set = self.request.GET.get("project_set")
        if project_set:
            queryset = queryset.filter(set=project_set)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_sets"] = (
            Project.objects.values_list("set", flat=True).distinct().order_by("set")
        )
        context["project_set"] = self.request.GET.get("project_set")
        return context


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
