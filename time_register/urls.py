from django.urls import path, include, re_path
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"tasks", views.TaskViewSet, basename="api_task")
router.register(r"work_entries", views.WorkEntryViewSet, basename="api_work_entry")

app_name = "time_register"
urlpatterns = [
    path("api/", include((router.urls, "api"), namespace="api_root")),
    re_path(
        r"^generic_test/(?P<resource>.*)/$",
        views.GenericTestViewSet.as_view(),
        name="api_generic_test",
    ),
    path("tasks/<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("", views.IndexView.as_view(), name="index"),
]

api_urls = router.urls
