from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"tasks", views.TaskViewSet, basename="api_task")
router.register(r"work_entries", views.WorkEntryViewSet, basename="api_work_entry")

app_name = "time_register"
urlpatterns = [
    path("api/", include((router.urls, "api"), namespace="api_root")),
    path("tasks/<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("", views.IndexView.as_view(), name="index"),
    path("react", views.index_react, name="index_react"),
]

api_urls = router.urls
