from django.contrib import admin
from .models import Tasks

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ["creado"]

admin.site.register(Tasks, TaskAdmin)