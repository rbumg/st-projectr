from django import template

from app.models.project import Project

register = template.Library()


@register.filter
def get_rate(project, day_type):
    try:
        rate = project.get_rate(day_type)
        return f"${rate:.2f}"
    except KeyError:
        return "Invalid rate"


@register.filter
def get_calculated_rate(project):
    try:
        rate = project.calculated_rate
        if rate is None:
            return "Not calculated"
        return f"${rate:.2f}"
    except KeyError:
        return "Unknown rate"


@register.filter
def get_project_set_total(project, project_set):
    try:
        total_reimbursement = sum(
            project.calculated_rate or 0
            for project in Project.objects.filter(set=project_set)
        )
        return f"${total_reimbursement:.2f}"
    except KeyError:
        return "Unknown rate"
