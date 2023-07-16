from django.views import generic
from rest_framework import viewsets
from rest_framework import generics

from .models import Task, WorkEntry, GenericTest
from .serializers import TaskSerializer, WorkEntrySerializer, GenericTestSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class WorkEntryViewSet(viewsets.ModelViewSet):
    serializer_class = WorkEntrySerializer
    queryset = WorkEntry.objects.all()


# TODO puts eu tenho que estudar melhor diferentes formas de fazer view neh
#       eu soh sei de maneira muito raza associado a model e serializer
#       mas nesse caso eu nao necessariamente preciso de serializer ai fica como hm
#       bom, eu posso colocar, just because.
# class GenericTestViewSet(viewsets.ModelViewSet):
class GenericTestViewSet(generics.CreateAPIView):
    serializer_class = GenericTestSerializer
    queryset = GenericTest.objects.all()

    def perform_create(self, serializer):
        resource = self.kwargs["resource"]
        data = self.request.data

        serializer.validated_data["resource"] = resource
        serializer.validated_data["data"] = data
        serializer.save()

        # na versao final do meu codigo acho que eu nao valido isso
        # é meio que o ponto
        # inclusive, ai nao faz mais sentido ter o serializer
        # mas se nao tiver o serializer, pra que eh que eu usei essa view
        # enfim.
        # serializer.save(resource=resource, data=data)


# # importante: o perplexity E O chatgpt nao tao se aproveitando do restvramework,
# # nao sei dizer se isso é um problema ou nao (acho que nao)
# # [ ] -deixa eu ver oqq tem dentor dessas viewsets e tal
# # [ ] -... ou... eu posso ter um model pra isso - mas é meio idiota
# #       pq pode ser que eu queira remover o model mas manter a view dps.
# class ThingyView(viewsets.GenericAPIView):
#     def post(self, request, *args, **kwargs):
#         resource = kwargs["resource"]
#         data = request.data
#         # Save data to the database
#         # ...
#         return Response({"success": True})


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
