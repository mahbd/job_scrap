from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'location', 'date_posted')
    search_fields = ('title', 'company', 'location')
    list_filter = ('date_posted', 'company')