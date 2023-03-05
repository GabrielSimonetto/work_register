from django.urls import path

from . import views

# TODO eu posso separar o API em router e o resto do site em nao-router

app_name = 'time_register'
urlpatterns = [
    path('api/task', views.TaskViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='api_task'),
    path('api/work_entry', views.WorkEntryViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='api_work_entry'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('', views.IndexView.as_view(), name='index'),
]


# urlpatterns = [
#     path('', views.IndexView.as_view(), name='index'),
#     path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#     # path('', views.IndexView.as_view(), name='index'),
# ]
