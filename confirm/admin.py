from django.conf.locale.pt_BR import formats as pt_BR_formats
from django.db.models import fields

pt_BR_formats.DATE_FORMAT = "d/m/Y"
pt_BR_formats.DATETIME_FORMAT = "d/m/Y H:i"

from django.contrib.admin.options import HORIZONTAL
from .models import Desconto

from .models import (
    GeneralManager,
    Town,
    Item,
    Inventory,
    ItemSale,
    Shop,
    ShoppingMall,
    Transaction,
    Checkout,
)

from .models import Desconto
from django.contrib import admin
from django.contrib.admin import ModelAdmin, VERTICAL

from django.utils.safestring import mark_safe
from django import forms

from admin_confirm.admin import AdminConfirmMixin, confirm_action
from .models import ShoppingMall
from django.contrib.admin.options import StackedInline

from django.core.exceptions import ValidationError
from django.forms import ModelForm

from mixins.export_csv import ExportCsvMixin
from mixins.confirmation import ConfirmationMixin
from mixins.confirmation_field_to_admin_form import add_confirm_field_to_admin_form

from .models import Checkout
from django.contrib.contenttypes.models import ContentType

class ItemAdmin(ConfirmationMixin, ModelAdmin, ExportCsvMixin):
    change_form_template = 'admin/confirma_submit/form_submit.html'
    # confirm_change = True
    # confirm_add = True
    # confirmation_fields = ("name", "price", "currency")
    radio_fields = {"currency": VERTICAL}

    list_display = ("name", "price", "currency")
    readonly_fields = ["image_preview"]

    save_as = True
    
    actions = ["export_as_csv"]

    search_fields = ['name',]

    def image_preview(self, obj):
        if obj.image:
            return mark_safe('<img src="{obj.image.url}" />')

class ShopAdmin(AdminConfirmMixin, ModelAdmin):
    confirmation_fields = ["name"]
    actions = ["show_message", "show_message_no_confirmation"]
    search_fields = ["name"]

    @confirm_action
    def show_message(modeladmin, request, queryset):
        shops = ", ".join(shop.name for shop in queryset)
        modeladmin.message_user(request, f"You selected with confirmation: {shops}")

    show_message.allowed_permissions = ("delete",)

    def show_message_no_confirmation(modeladmin, request, queryset):
        shops = ", ".join(shop.name for shop in queryset)
        modeladmin.message_user(request, f"You selected without confirmation: {shops}")

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class InventoryAdmin(ModelAdmin):
    list_display = ("shop", "item", "quantity")

    readonly_fields = ['notes',]

    fieldsets = (
        (None, {
            'fields': ('confirmation_field',),
        }),
        ('Dados', {
            'fields': ('shop', 'item', 'quantity', 'notes',),
        }),
    )

    form = add_confirm_field_to_admin_form(Inventory)

    # def has_add_permission(self, request):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_view_permission(self, request, obj=None):
    #     return True

    class Media:
        css = {"all": ('css/adm_loader.css',)}
        js = ('admin/js/jquery.init.js', 'js/adm_loader.js', 'js/adm_confirmation_field_to_admin_form.js',)

class GeneralManagerAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirm_add = True
    save_as = True
    search_fields = ["name"]

class TownAdmin(ModelAdmin):
    search_fields = ["name"]

class ShopInline(StackedInline):
    model = ShoppingMall.shops.through


class ShoppingMallAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_add = True
    confirm_change = True
    confirmation_fields = ["name"]

    inlines = [ShopInline]
    raw_id_fields = ["general_manager"]


class TransactionAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_add = True
    confirm_change = True

class ItemSaleAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_add = True
    confirm_change = True
    autocomplete_fields = ['desconto',]


class CheckoutForm(ModelForm):
    search_fields = ["shop", "date"]
    confirm_change = True

    class Meta:
        model = Checkout
        fields = [
            "currency",
            "shop",
            "total",
            "timestamp",
            "date",
        ]

    def clean_total(self):
        try:
            total = float(self.cleaned_data["total"])
        except:
            raise ValidationError("Invalid Total From clean_total")
        if total == 111:  # Use to cause error in test
            raise ValidationError("Invalid Total 111")

        return total

    def clean(self):
        try:
            total = float(self.data["total"])
        except:
            raise ValidationError("Invalid Total From clean")
        if total == 222:  # Use to cause error in test
            raise ValidationError("Invalid Total 222")

        self.cleaned_data["total"] = total
class CheckoutAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_add = True
    confirm_change = True
    autocomplete_fields = ["shop"]
    form = CheckoutForm

#  * * * * * * * * * * * * * * * * * * * * * * * ** * * * * * * * * * * * * * * * * * * * * * * *

# class DescontoAdminForm(forms.ModelForm):
#     class Meta:
#         model = Desconto
#         fields = [
#             'item', 
#             'descricao', 'percentual', 'cupom',
#             'validade',
#         ]


class ItemSaleDescontoInline(admin.StackedInline):

    # def has_add_permission(self, request, obj=None):
    #     return False

    readonly_fields = ['item', 'quantity', 'total', 'currency', 'desconto', 'transaction']

    model = ItemSale
    extra = 0
    show_change_link = True


class DescontoAdmin(ConfirmationMixin, ExportCsvMixin, admin.ModelAdmin,):
    # class DescontoAdmin(admin.ModelAdmin, ExportCsvMixin):
    change_form_template = 'admin/confirma_submit/form_submit.html'
    # form = DescontoAdminForm
    search_fields = ('descricao',)
    radio_fields = {"cupom": HORIZONTAL}

    inlines = [ItemSaleDescontoInline,]

    # save_as = True

    actions = ["export_as_csv"]

    autocomplete_fields = ['item',]
    class Media:
        css = {"all": ('css/adm_field_sets.css',)}
    
    fieldsets = (
        (None, {
            'classes': ('div_inline_group', 'stack_labels', 'stack_ul_errorlist', 'stack_div_help', 'stack_div_readonly',),
            'fields': ((
                'item', 
                'item_dois',
                'descricao', 
                'percentual', 'cupom',
                ),
                ('validade',),
                ('no_cartao',),
            ),
        }),
    )

    # fields = (('item', 'descricao', 'percentual', 'cupom',),
    #           ('validade',),
    #           ('no_cartao',),
    # )

    readonly_fields =  ('no_cartao',)   

    # def changeform_view(self, request, object_id, form_url='', extra_context=None):
        # return super().changeform_view(request, object_id, form_url, extra_context)        

admin.site.register(Item, ItemAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(ShoppingMall, ShoppingMallAdmin)
admin.site.register(GeneralManager, GeneralManagerAdmin)
admin.site.register(Town, GeneralManagerAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(ItemSale, ItemSaleAdmin)
admin.site.register(Checkout, CheckoutAdmin)

admin.site.register(Desconto, DescontoAdmin)

# available_apps =  
# {
#     'name': 'Confirm', 
#     'app_label': 'confirm', 
#     'app_url': '/admin/confirm/', 
#     'has_module_perms': True, 
#     'models': 
#         [
#             {
#                 'name': 'Descontos', 
#                 'object_name': 'Desconto',
#                 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 
#                 'admin_url': '/admin/confirm/desconto/', 
#                 'add_url': '/admin/confirm/desconto/add/', 
#                 'view_only': False
#             }, 
#             {
#                 'name': 'Items', 
#                 'object_name': 'Item', 
#                 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 
#                 'admin_url': '/admin/confirm/item/', 
#                 'add_url': '/admin/confirm/item/add/', 
#                 'view_only': False
#             }
#          ]
# }