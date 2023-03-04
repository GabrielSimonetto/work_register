from django.utils import timezone
from django.views import generic
from django.http import HttpResponse
from rest_framework import viewsets

from .models import Task, WorkEntry
from .serializers import TaskSerializer, WorkEntrySerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class WorkEntryViewSet(viewsets.ModelViewSet):
    serializer_class = WorkEntrySerializer
    queryset = WorkEntry.objects.all()


# def index(request):
#     # TODO: show all tasks
#     # TODO: tbm acho descolado apresentar todas as urls validas soh pq sim.
#     return HttpResponse("Hello, world. You're at the polls index.")
class IndexView(generic.ListView):
    template_name = 'time_register/index.html'
    context_object_name = 'latest_task_list'

    def get_queryset(self):
        """
        Return the last five published tasks (not including those set to be
        published in the future).
        """
        # TODO delete
        # return Task.objects.filter(
        #     pub_date__lte=timezone.now()
        # ).order_by('-pub_date')[:5]
        return Task.objects.all()


# TODO isso nao eh "detail"
#       deixa eu ver se eu acho uma lista desse generic views
#       pra entender se ele demonstra oqq eh cada uma dessas classes
class DetailView(generic.DetailView):
    model = Task
    template_name = 'time_register/detail.html'
    # context_object_name = 'task'

    # # Aqui eu tenho que dar um jeito de pegar um task em especifico,
    # #    e ai eu vou mostrar os timestamps relacionados a ele.
    # def get_queryset(self):
    #     """
    #     Return the last five published tasks (not including those set to be
    #     published in the future).
    #     """
    #     # return Task.objects.all()
    #     return Task.objects.all()[0].workentry_set.all()

#     # def get_queryset(self):
#     #     """
#     #     Excludes any questions that aren't published yet.
#     #     """
#     #     return Question.objects.filter(pub_date__lte=timezone.now())
