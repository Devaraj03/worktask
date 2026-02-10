from django.contrib import admin
from .models import Work, WorkStatus


class WorkStatusInline(admin.TabularInline):
    model = WorkStatus
    extra = 0


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [WorkStatusInline]


admin.site.register(WorkStatus)
