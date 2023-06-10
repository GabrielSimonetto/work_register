from django.contrib import admin

# from django.contrib.auth.models import Permission

from django.contrib.auth.models import User, Permission

from .models import Task, WorkEntry
from simple_history.admin import SimpleHistoryAdmin


class TaskHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "name", "status"]
    history_list_display = ["goal_daily_minutes"]
    search_fields = ["name", "user__username"]

    def change_user_permissions(self, request, queryset):
        user = User.objects.get(username="admin")

        # Clear existing permissions
        user.user_permissions.clear()

        # Add desired permissions
        user.user_permissions.add(
            Permission.objects.get(codename="view_poll"),
            Permission.objects.get(codename="change_poll"),
        )

    change_user_permissions.short_description = "Change user permissions"


admin.site.register(Task, TaskHistoryAdmin)
admin.site.register(WorkEntry, SimpleHistoryAdmin)
