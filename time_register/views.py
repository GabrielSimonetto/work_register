from django.views import generic
from rest_framework import viewsets

from .models import Task, WorkEntry
from .serializers import TaskSerializer, WorkEntrySerializer

from django.shortcuts import render


def index_react(request):
    return render(request, "index.html")


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class WorkEntryViewSet(viewsets.ModelViewSet):
    serializer_class = WorkEntrySerializer
    queryset = WorkEntry.objects.all()


class IndexView(generic.ListView):
    template_name = "time_register/index.html"
    context_object_name = "latest_task_list"

    def get_queryset(self):
        """
        Return the last five published tasks (not including those set to be
        published in the future).
        """
        return Task.objects.all()


class DetailView(generic.DetailView):
    model = Task
    template_name = "time_register/detail.html"
