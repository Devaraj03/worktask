from django.views.generic import (ListView,
CreateView, UpdateView, DeleteView,TemplateView)
from django.urls import reverse_lazy
from .models import Work, WorkStatus
from .forms import WorkForm
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import models


class KanbanView(TemplateView):
    template_name = "worktrack/kanban.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["columns"] = [
            {
                "key": "OPEN",
                "title": "Open",
                "items": WorkStatus.objects
                    .filter(state="OPEN")
                    .select_related("work", "work__assigned_to")
            },
            {
                "key": "IN_PROGRESS",
                "title": "In Progress",
                "items": WorkStatus.objects
                    .filter(state="IN_PROGRESS")
                    .select_related("work", "work__assigned_to")
            },
            {
                "key": "CLOSED",
                "title": "Closed",
                "items": WorkStatus.objects
                    .filter(state="CLOSED")
                    .select_related("work", "work__assigned_to")
            },
        ]
        return context

class WorkCreateView(CreateView):
    model = Work
    form_class = WorkForm
    template_name = 'worktrack/work_form.html'
    success_url = reverse_lazy('kanban')

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user

        response = super().form_valid(form)

        # Get last position in OPEN column
        last_position = (
            WorkStatus.objects
            .filter(state='OPEN')
            .aggregate(models.Max('position'))
            .get('position__max') or 0
        )

        WorkStatus.objects.create(
            work=self.object,
            state='OPEN',
            position=last_position + 1
        )
        return response


class WorkUpdateView(UpdateView):
    model = Work
    form_class = WorkForm
    template_name = 'worktrack/work_form.html'
    success_url = reverse_lazy('kanban')


class WorkDeleteView(DeleteView):
    model = Work
    template_name = 'worktrack/work_confirm_delete.html'
    success_url = reverse_lazy('kanban')


@require_POST
def update_status(request):
    data = json.loads(request.body)

    status_id = data.get("status_id")
    new_state = data.get("state")
    new_position = data.get("position")

    status = WorkStatus.objects.get(id=status_id)

    # If moved to a new column
    if status.state != new_state:
        status.state = new_state

        # Reset closed_at if reopened
        if new_state != 'CLOSED':
            status.closed_at = None

    status.position = new_position
    status.save()

    return JsonResponse({"success": True})
