from django.contrib import admin
from .models import *


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'budget', 'total_transactions', 'budget_left']
    # list_display_links = ['name', 'budget', 'total_transactions', 'budget_left']
    list_editable = ['budget']
    search_fields = ['name']
    list_filter = ['name', 'budget']

admin.site.register(Project, ProjectAdmin)
admin.site.register(Expense)
admin.site.register(Category)


admin.site.site_header = "Budget App"
admin.site.site_title = "Budget App"