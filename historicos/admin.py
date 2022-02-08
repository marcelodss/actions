from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION

from .views import format_change_message

from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display_links = None

    list_per_page = 10
    list_max_show_all = 0

    list_filter = [
        'user',
        'action_flag',
        'content_type',
        # 'object_id'
    ]

    list_display = [
        'action_time',
        'action_flag',
   
        'content_type',
        'object_link',
  
        'action_description',
        'user',
    ]

    fields = list_display
    readonly_fields = fields

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return True

    def action_description(self, obj):
        return format_change_message(obj.change_message)
    action_description.short_description = "Descrição da Ação"

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    # object_link.admin_order_field = "object_repr"
    object_link.short_description = "Objeto"

 



