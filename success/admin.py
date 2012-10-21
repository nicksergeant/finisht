from django.contrib import admin
from finisht.success.models import Success

class SuccessAdmin(admin.ModelAdmin):
    list_display = ('description',)
    ordering = ('completed_on',)

admin.site.register(Success, SuccessAdmin)
