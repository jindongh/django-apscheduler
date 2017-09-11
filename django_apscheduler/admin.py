import datetime
from django.contrib import admin
from django.utils.timezone import now

from django_apscheduler.models import DjangoJob, DjangoJobExecution
from django.db.models import Avg

def execute_now(ma, r, qs):
    for item in qs:
        item.next_run_time=now()
        item.save()

execute_now.short_description = "Force execute tasks right now"


class DjangoJobAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "next_run_time", "average_duration"]
    actions = [execute_now]
    def get_queryset(self, request):
        self._durations = {
            item[0]: item[1]
            for item in DjangoJobExecution.objects.filter(
                status=DjangoJobExecution.SUCCESS,
                run_time__gte=now()-datetime.timedelta(days=2)
            ).values_list("job").annotate(duration=Avg("duration"))
        }
        return super(DjangoJobAdmin, self).get_queryset(request)

    def average_duration(self, obj):
        return self._durations.get(obj.id) or 0



class DjangoJobExecutionAdmin(admin.ModelAdmin):
    list_display = ["id", "job", "html_status", 'retval', "run_time", "duration"]

    list_filter = ["job__name", "run_time", "status"]

    def get_queryset(self, request):
        return super(DjangoJobExecutionAdmin, self).get_queryset(
            request
        ).select_related("job")

admin.site.register(DjangoJob, DjangoJobAdmin)
admin.site.register(DjangoJobExecution, DjangoJobExecutionAdmin)
