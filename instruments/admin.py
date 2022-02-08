# Passando parâmetros para a ação administrativa do Django
# Fonte : https://www.agiliq.com/blog/2014/08/passing-parameters-to-django-admin-action/

from django.contrib import admin

from django.conf.locale.pt_BR import formats as pt_BR_formats
pt_BR_formats.DATE_FORMAT = "d/m/Y"
pt_BR_formats.DATETIME_FORMAT = "d/m/Y H:i"

from django.contrib.admin.helpers import ActionForm
from django import forms

from django.contrib.admin import widgets   

from django.contrib import messages
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.widgets import AdminDateWidget
from django.db.models.indexes import Index

from django.utils.html import format_html
from django.urls import reverse

from .models import (Instrument, validate_price_100_200)

from django.db.models import F

from django.http import HttpResponseRedirect

from django.urls import path

from django.shortcuts import render, get_object_or_404

from django.utils.safestring import mark_safe

def update_price_na_change_list(modeladmin, request, queryset):
    price_ini = request.POST['price_ini']
    price_fim = request.POST['price_fim']
    if price_ini == None:
        price_ini = 0
    elif not price_ini.isdigit():
        price_ini = 0
    elif price_ini == None:
        price_ini = 0
    elif type(price_ini) is float:
        price_ini = 0
    else:
        price_ini = int(price_ini) 
    if price_fim == None:
        price_fim = 0
    elif not price_fim.isdigit():
        price_fim = 0
    elif price_fim == None:
        price_fim = 0
    elif type(price_fim) is float:
        price_fim = 0
    else:
        price_fim = int(price_fim) 
    
    if price_ini <= price_fim:
        queryset.update(price = int(price_ini) * int(price_fim))
        modeladmin.message_user(request, ("Sucesso na Atualização de %d linha(s)") % (queryset.count(),), messages.SUCCESS) 
    else:
        modeladmin.message_user(request, ("Informe ini ou fim maior que zero"), messages.ERROR)  
update_price_na_change_list.short_description = 'atualizar preços com campos na change list'
update_price_na_change_list.allowed_permissions = ('change', )


class UpdateActionForm(ActionForm):
    price_ini = forms.IntegerField(required=False, label="Valor Inicial: ", initial=0)
    price_fim = forms.IntegerField(required=False, label="Valor Final: ", initial=0)
 
    date_tst = forms.DateField(required=False, label="Data: ", widget=AdminDateWidget())
    mydate = forms.DateField(required=False, widget=widgets.AdminDateWidget)
 
class InstrumentAdmin(admin.ModelAdmin):
    change_list_template = 'admin/instruments/instrument/change_list_instrument.html'
    action_form = UpdateActionForm
    actions = [update_price_na_change_list]
    list_filter = ('name',)
    list_display = ('name', 'price', 'data')
    list_editable = ('price',)
    
    readonly_fields = ('admin_unit_details', 'link_field', 'button_field', 'button_teste', ) # readonly_fields é necessário para evitar a validação do campo
    fields = ['admin_unit_details', 'link_field', 'name', 'price', 'data', 'button_field', 'button_teste',]

    # remover campos condicionalmente usando fieldsets
    # fonte: http://es.uwenku.com/question/p-ekgaairz-bk.html
    def get_fieldsets(self, request, obj=None): 
        fieldset_existing = (
            (None, { 
            'classes': ('wide',), 
            'fields': ('admin_unit_details', 'link_field','data', 'name', 'price', 'button_field', 'button_teste',)} 
            ), 
        ) 
        fieldset_new = (
            (None, { 
            'classes': ('wide',), 
            'fields': ('data', 'name', 'price',)} 
            ), 
        ) 
        if obj is None: 
            # durante a adição; add; (não tem id) 
            return fieldset_new 
        elif obj and not request.user.has_perm(self.model._meta.app_label + '.change_' + self.opts.model_name): 
            # durante a alteração; change; (tem id) 
            return fieldset_new 
        return fieldset_existing 

    # # remover campos condicionalmente usando field
    # # fonte: https://stackoverflow.com/questions/54881688/django-admin-how-to-hide-a-specific-model-field-during-view-and-edit
    # def get_fields(self, request, obj=None):
    #     field_existing = super().get_fields(request, obj)
    #     field_new = ['name', 'price', 'data',]
    #     if obj is None: 
    #         # durante a adição; add; (não tem id)
    #         fields = field_new
    #     elif obj and not request.user.has_perm(self.model._meta.app_label + '.change_' + self.opts.model_name): 
    #         # durante a alteração; change; (tem id) AND sem permissão change 
    #         fields = field_new
    #     else:
    #         fields = field_existing
    #     return fields    

    @mark_safe
    def link_field(self, obj):
        link_url = reverse('intrument_detalhe', args=[obj.pk])
        return '<a href="{link_url}" target="_blank">Detalhe para {link_text}</a>'.format(
            link_url=link_url, 
            #  user=car.owner.fullname
            link_text=obj
        )
    link_field.short_description = ""

    @mark_safe
    def button_field(self, request, obj=None):
        html = '<input type="submit" value="Deleta Iguais e Preço 100" name="_make_price_cem"/>'
        return html
    button_field.short_description = ""
    
    @mark_safe
    def button_teste(self, request, obj=None):
        html = '<input type="submit" value="Teste" name="_teste_x"/>'
        return html
    button_teste.short_description = ""

    def get_list_display(self, request):
        list_display = super(InstrumentAdmin, self).get_list_display(request)
        if request.user.has_perm(self.model._meta.app_label + '.change_' + self.opts.model_name):
            list_display = ('name', 'price', 'data','detalhe_link', 'detalhe_lista', 'deletar_em_linha',)
        return list_display

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('zerar_precos/', self.admin_site.admin_view(self.set_zerar_precos)),
            path('dobrar_precos/', self.admin_site.admin_view(self.set_dobrar_precos)),
            path('<int:pk>/detalhe/', self.admin_site.admin_view(self.detalhe)),
        ]
        return my_urls + urls

    def detalhe(self, request, pk):
        if request.user.has_perm(self.model._meta.app_label + '.view_' + self.opts.model_name):
            instrument = get_object_or_404(Instrument, pk=pk)
            template_detalhe = 'admin/instruments/instrument/detalhe_instrument.html'
            return render(request, template_detalhe, {
                'instrument': instrument,
                'title': "Detalhe",
                'app_label': self.model._meta.app_label,
                'app': self.opts.app_label,
                'modelo': self.opts.model_name,
                'opts': self.model._meta,
            })
        else:
            link = "{}{}/{}/".format(reverse('admin:index'), self.model._meta.app_label, self.opts.model_name)
            self.message_user(request, "Acesso Negado a Detalhe de " + self.model._meta.verbose_name_plural + ".", messages.ERROR)
            return HttpResponseRedirect(redirect_to=link)
    
    def detalhe_lista(self, obj):
        link = reverse('intrument_detalhe', args=[obj.pk])
        html = '<input type="button" onclick="location.href=\'{}\'" value="Detalhe" />'.format(link)
        return format_html(html)       
    detalhe_lista.short_description = 'Detalhes Button'
  
    def detalhe_link(self, obj):
        link = reverse('intrument_detalhe', args=[obj.pk])
        html = '<a href="{}\">Detalhe</a>'.format(link)
        return format_html(html)       
    detalhe_link.short_description = 'Detalhes Link'
    
    def set_zerar_precos(self, request):
        if request.user.has_perm(self.model._meta.app_label + '.change_' + self.opts.model_name):
            self.model.objects.all().update(price=0)
            self.message_user(request, "Todos os Preços foram Zerados", messages.SUCCESS)
            return HttpResponseRedirect("../")
        else:
            self.message_user(request, "Acesso Negado para a opção 'Zerar Preços'.", messages.ERROR)
            return HttpResponseRedirect("../")

    def set_dobrar_precos(self, request):
        if request.user.has_perm(self.model._meta.app_label + '.change_' + self.opts.model_name):
            self.model.objects.all().update(price=((F('price')) + 1) * 2)
            self.message_user(request, "Todos os Preços foram Dobrados")
            return HttpResponseRedirect("../")
        else:
            self.message_user(request, "Acesso Negado para a opção 'Dobrar Preços Preços'.", messages.ERROR)
            return HttpResponseRedirect("../")

    def deletar_em_linha(self, obj):
        # Ações personalizadas em objetos individuais (botão de exclusão disponível para objetos individuais)
        # Fonte: https://django-tips.avilpage.com/en/latest/admin_custom_admin_actions.html#custom-actions-on-individual-objects
        view_name = "admin:{}_{}_delete".format(obj._meta.app_label, obj._meta.model_name)
        link = reverse(view_name, args=[obj.pk])
        html = '<input type="button" onclick="location.href=\'{}\'" value="Delete" />'.format(link)
        return format_html(html)
        # Ver, também: 
        #  -> Como adicionar um botão personalizado à página de mudança de visualização (change view page) do Django?
        # Fonte: https://books.agiliq.com/projects/django-admin-cookbook/en/latest/custom_button.html
        # -> Como adicionar botões de ação personalizados (não ações) à página de lista do Django Admin?
        # Fonte: https://books.agiliq.com/projects/django-admin-cookbook/en/latest/action_buttons.html
 
     # Adicionar um botão personalizado à página de mudança de visualização do Django
    # fonte: https://books.agiliq.com/projects/django-admin-cookbook/en/latest/custom_button.html
    
    def response_change(self, request, obj):
        if "_make_price_mil" in request.POST:
            preco = 1000
            # nomes_correspondentes_exceto_este == objetos com nomes duplicadados exceto (.exclude) o atual.
            nomes_correspondentes_exceto_este = self.get_queryset(request).filter(name=obj.name).exclude(pk=obj.id)
            obj.price = preco
            obj.save()
            # nomes_correspondentes_exceto_este == apagar, deletar.
            tot_delete = nomes_correspondentes_exceto_este.delete()
             # altera preço do atual
            tot_delete = tot_delete[0]
            mensagem = str(obj.name) + " com ID=" + str(obj.pk) + " agora é único e seu preço passou a ser " + str(preco) + "; " + str(tot_delete) + " deletado(s)"
            self.message_user(request, (mensagem), messages.SUCCESS)
            return HttpResponseRedirect(".")  
        
        if "_make_price_cem" in request.POST: 
            preco = 100
            # nomes_correspondentes_exceto_este == objetos com nomes duplicadados exceto (.exclude) o atual.
            nomes_correspondentes_exceto_este = self.get_queryset(request).filter(name=obj.name).exclude(pk=obj.id)

            valida = validate_price_100_200(preco)
            if  valida["retorno"] == True:
                obj.price = preco
                obj.save()
                # nomes_correspondentes_exceto_este == apagar, deletar.
                tot_delete = nomes_correspondentes_exceto_este.delete()
                # altera preço do atual
                tot_delete = tot_delete[0]
                mensagem = str(obj.name) + " com ID=" + str(obj.pk) + " agora é único e seu preço passou a ser " + str(preco) + "; " + str(tot_delete) + " deletado(s)"
                self.message_user(request, (mensagem), messages.SUCCESS)
            else:
                mensagem = str(valida["mensagem"]) + " " + str(obj.name) + " com ID=" + str(obj.pk) + " mantido com preço = " + str(obj.price) + ". Zero deletados"
                self.message_user(request, (mensagem), messages.ERROR)
            return HttpResponseRedirect(".")  

        # xxx
        if "_teste_x" in request.POST: 
            self.message_user(request, ("Em Desenvolvimento"), messages.ERROR)
            return HttpResponseRedirect(".")  
        # xxx
        return super().response_change(request, obj)

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['pk_do_modelo'] = object_id 
        # # Mantido para fins didáticos
        # if request.user.has_perm(self.model._meta.app_label + '.view_' + self.opts.model_name):
        #     extra_context['perm_view'] = 'ok' 
        # if request.user.has_perm(self.model._meta.app_label + '.add_' + self.opts.model_name):
        #     extra_context['perm_add'] = 'ok' 
        # if request.user.has_perm(self.model._meta.app_label + '.change_' + self.opts.model_name):
        #     extra_context['perm_change'] = 'ok' 
        # if request.user.has_perm(self.model._meta.app_label + '.delete_' + self.opts.model_name):
        #     extra_context['perm_delete'] = 'ok' 
        return super().change_view(request, object_id, extra_context=extra_context,)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['so_para_exemplificar'] = "Só para exemplificar"
        # # Mantido para fins didáticos
        # if request.user.has_perm(self.model._meta.app_label + '.view_' + self.opts.model_name):
        #     extra_context['perm_view'] = 'ok' 
        # if request.user.has_perm(self.model._meta.app_label + '.add_' + self.opts.model_name):
        #         extra_context['perm_add'] = 'ok' 
        # if request.user.has_perm(self.model._meta.app_label + '.change_' + self.opts.model_name):
        #     extra_context['perm_change'] = 'ok' 
        # if request.user.has_perm(self.model._meta.app_label + '.delete_' + self.opts.model_name):
        #     extra_context['perm_delete'] = 'ok' 
        return super().changelist_view(request, extra_context=extra_context,)

    # Substituindo (globalmente) o sufixo do rótulo do campo no Django
    # Fontes: 
    # https://medium.com/@MatheusCAS/overriding-globally-field-label-suffix-in-django-ed3ffb10af7
    # https://stackoverflow.com/questions/66157466/how-to-change-label-caption-of-readonly-item-in-django-admin
    def get_form(self, request, obj=None, **kwargs):
        form_requerido = super(InstrumentAdmin, self).get_form(request, obj, **kwargs)
        for field in form_requerido.base_fields:
            if form_requerido.base_fields.get(field).required:
                form_requerido.base_fields.get(field).label_suffix = "   * ;o)"
            if field == 'name':
                form_requerido.base_fields['name'].label_suffix = ' com  _suffix alterado'
                form_requerido.base_fields['name'].widget.attrs['style'] = 'width: 4em;'

        # for f in self.fields:
        #     if f not in self.readonly_fields:
        #         print(f'->>>> Disponível: {f}')


        # Não aplique o exemplo abaixo para 'label' em forms/field readonly porque causará um erro.
        # Se o seu campo somente leitura for um campo do model, utilize o atributo verbose_name.
        # if 'name' in form_requerido.base_fields:
        #     print('tem name')
        # else:
        #     ('name tem não')
        return form_requerido

admin.site.register(Instrument, InstrumentAdmin)
 