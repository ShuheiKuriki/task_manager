from django.contrib import admin

# Register your models here.
from .models import Update
import logging

logger = logging.getLogger(__name__)
# logger.error('admin')
def notify_line(modeladmin, request, queryset):
    for update in queryset:

        logger.error(update.title)
        update.line_push(request)
#
class UpdateAdmin(admin.ModelAdmin):
    actions = [notify_line]


notify_line.short_description = '通知を送信する'
admin.site.register(Update, UpdateAdmin)