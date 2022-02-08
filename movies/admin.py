# Passando parâmetros para a ação administrativa do Django
font_awesome = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
from django.contrib import admin
from django.conf.locale.pt_BR import formats as pt_BR_formats
pt_BR_formats.DATE_FORMAT = "d/m/Y"
pt_BR_formats.DATETIME_FORMAT = "d/m/Y H:i"

from django.utils import timezone

from django.db.models import query

from .models import (Movie, Genre, validate_genero)

from django.contrib.admin.helpers import ActionForm
from django import forms

from django.contrib import messages
from django.utils.translation import ngettext

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import GenreFormComSave, GenreFormComUpdate

from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin import helpers

from mixins.confirmation import ConfirmationMixin

class ParametroForm(ActionForm): # para action com parâmetro(s)
    parametro = forms.IntegerField(required=False, label="Parâmetro: ", initial=0)

# class MovieInline(admin.StackedInline):
class MovieInline(admin.TabularInline):
    model = Movie
    # template = 'admin/movies/genre/inline/stacked.html'
    extra = 0
    show_change_link = True
    ordering = ['-id']
    verbose_name = "Filme"
    verbose_name_plural = "Filmes"
    
    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

class GenreAdmin(ConfirmationMixin, admin.ModelAdmin):
    save_on_top = True
    inlines = [MovieInline,]
    fields = ['title', 'data', 'new_score', 'usuario', ]
    # readonly_fields = ['title', ]

    def has_add_permission(cls, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        css = {"all": ('css/adm_loader.css', font_awesome, 'css/adm_modal.css',)}
        js = ('admin/js/jquery.init.js', 'js/adm_loader.js', 'js/adm_modal.js')

    def response_change(self, request, obj):
        if "_add_movie" in request.POST:
            # preco = 1000
            # # nomes_correspondentes_exceto_este == objetos com nomes duplicadados exceto (.exclude) o atual.
            # nomes_correspondentes_exceto_este = self.get_queryset(request).filter(name=obj.name).exclude(pk=obj.id)
            # obj.price = preco
            # obj.save()
            # # nomes_correspondentes_exceto_este == apagar, deletar.
            # tot_delete = nomes_correspondentes_exceto_este.delete()
            #     # altera preço do atual
            # tot_delete = tot_delete[0]
            
            Movie.objects.create(title='Filme xxx', genre=obj, score=obj.new_score, data=obj.data)
            mensagem = str(obj.title) + ", ID: " + str(obj.pk) +" Adicionado."
            self.message_user(request, (mensagem), messages.SUCCESS)
            return HttpResponseRedirect(".")  

        if "_add_movie_modal" in request.POST:
            Movie.objects.create(title='Filme xxx', genre=obj, score=obj.new_score, data=obj.data)
            mensagem = str(obj.title) + ", ID: " + str(obj.pk) +" Adicionado (VIA MODAL)."
            self.message_user(request, (mensagem), messages.SUCCESS)
            return HttpResponseRedirect(".") 

        return super().response_change(request, obj)

class MovieAdmin(admin.ModelAdmin):
    change_form_template = 'admin/movies/movie/change_form_ajax.html'
    list_display = ('title', 'genre', 'score', 'status', 'data', 'hora', 'data_hora',)
    list_filter = ('title', 'genre', 'score', 'status', 'data', 'hora', 'data_hora',)
    actions = ['set_genre_action_001', 'set_genre_action_002', 
                'set_score_action_001', 
                'update_status_001_param_fixo_template_exclusivo', 'update_status_002_param_fixo_template_generico',]
    fields = ['title', 'genre', 'score', 'status', 'data', 'hora', 'data_hora',]
    readonly_fields = ['genre',]

    def has_add_permission(cls, request):
            return False

    class Media:
        js = ('admin/js/jquery.init.js', 'js/adm_ajax_confirm.js')


    # **********************************************
    # Action com parâmetro(s)
    # **********************************************
    action_form = ParametroForm    

    # Alterar scores
    # fonte: https://en.proft.me/2015/01/29/admin-actions-django-custom-form/
    # **********************************************
    def set_score_action_001(self, request, queryset):
        score = int(request.POST['parametro'])
        queryset.update(score=score)
        ct = ContentType.objects.get_for_model(queryset.model) # for_model --> get_for_model
        for obj in queryset:
            LogEntry.objects.log_action( # log_entry --> log_action
                user_id = request.user.id,
                content_type_id = ct.pk,
                object_id = obj.pk,
                object_repr = obj.title,
                action_flag = CHANGE, # actions_flag --> action_flag
                change_message = 'Atualizou Score.')

        messages.success(request, '{0} movie(s) com score(s) atualizado(s)'.format(queryset.count()))
    set_score_action_001.short_description = u'Atualizar Score 001 - com parâmetro em change_list e LogEntry'  


    # **********************************************
    # Action com formulário em página intermediária
    # **********************************************

    # Alterar gênero - Utilizando Save()
    # fonte: https://en.proft.me/2015/01/29/admin-actions-django-custom-form/
    
    # Atualizando vários objetos sequencialemente - obj.save()
    # fonte: https://docs.djangoproject.com/en/3.2/topics/db/queries/#updating-multiple-objects-at-once
    # **********************************************
    def set_genre_action_001(self, request, queryset):
        # Observe o input type hidden name="action" recebendo value = "o nome desta action" no template html 
        # <input type="hidden" name="action" value="set_genre_action_001">
        erros = None
        updated = 0
        post_action ='do_action' 
        action_name = 'set_genre_action_001' 
        if post_action in request.POST:
            # Observe o value do input type hidden name="do_action" recebendo value="yes" no template html 
            # <input type="hidden" name="do_action" value="yes">
            form = GenreFormComSave(request.POST)
            if form.is_valid():
                genre = form.cleaned_data['genre']
                valida = validate_genero(genre)
                if valida["retorno"] == True:
                    # updated = queryset.update(genre=genre)
                    for obj in queryset:
                        obj.genre = genre
                        obj.save()
                        updated = updated + 1
                    self.message_user(request, ngettext(
                        '%d filme atualizado para ' + str(genre),
                        '%d filmes atualizados para ' + str(genre),
                        updated,) % updated, 
                        messages.SUCCESS)  # messages.success(request, '{0} '.format(updated))
                    return
                else:
                    erros = valida["mensagem"] 
            else:
                print(form.errors) 
        else:
            form = GenreFormComSave()

        #  O modelo 'admin/includes/fieldset.html' exibe os campos do formulário no mesmo formato que admin/change_form.html
        #  Fonte: https://www.dmertl.com/blog/?p=116 
        adminform = helpers.AdminForm(form, list([(None, {'fields': form.base_fields})]),
                                      self.get_prepopulated_fields(request))
        tot_queryset = queryset.count()
        if tot_queryset > 1:
            question = "Alterar o Gênero para os Filmes listados abaixo:"
        else:
            question = "Alterar o Gênero para o Filme listado abaixo:"
        
        campos_tupla =   queryset.values_list('pk', 'title', 'genre__title', 'data', 'data_hora', named=True)
        campos_lista =   queryset.values_list('pk', 'title', 'genre__title', 'data', 'data_hora')

        cabecalho_list = ['title', 'genre__title', 'data', 'data_hora']
        corpo_list = campos_lista
      
        dados = {'cabecalho_list': cabecalho_list, 'corpo_list': corpo_list,}
        
        return render(request, 'admin/actions/actions_ordinary.html',
            {
             'dados': dados,
             'title': "Atualizar Gênero",
             'question': question,
             'campos_tupla': campos_tupla,
             'campos_lista': campos_lista,
             'tot_queryset': tot_queryset,
             'form': form,
             'app_label': self.model._meta.app_label,
             'app': self.opts.app_label,
             'modelo': self.opts.model_name,
             'opts': self.model._meta,
             'erros': erros,
             'has_change_permission': self.has_change_permission(request),
             'has_permission': self.has_change_permission(request), # necessário para exibir {% block usertools %}
             'adminform': adminform,
             'post_action': post_action,
             'action_name': action_name,
            })
    set_genre_action_001.short_description = u'Atualizar Gêneros - Utilizando Save()'
    set_genre_action_001.allowed_permissions = ('change', )

    # X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X 
    # Atualizando vários objetos COM UPDATE
    # fonte: https://docs.djangoproject.com/en/3.2/topics/db/queries/#updating-multiple-objects-at-once
    # **********************************************
    def set_genre_action_002(self, request, queryset):
        post_action ='do_action' 
        action_name = 'set_genre_action_002' 
        # Observe o input type hidden name="action" recebendo value = "o nome desta action" no template html 
        # <input type="hidden" name="action" value="set_genre_action_002">
        if post_action in request.POST:
            # Observe o value do input type hidden name="do_action" recebendo value="yes" no template html 
            # <input type="hidden" name="do_action" value="yes">
            form = GenreFormComUpdate(request.POST)
            if form.is_valid():
                genre = form.cleaned_data['genre']
                updated = queryset.update(genre=genre)
                self.message_user(request, ngettext(
                    '%d filme atualizado para ' + str(genre),
                    '%d filmes atualizadospara ' + str(genre),
                    updated,) % updated, 
                    messages.SUCCESS)  # messages.success(request, '{0} '.format(updated))
                return
        else:
            form = GenreFormComUpdate()

        tot_queryset = queryset.count()
        if tot_queryset > 1:
            question = "Alterar o Gênero para os " + str(tot_queryset) + " Filmes Listados?"
            objects_caption = "Filmes Selecionados para Alteração de Gênero"
        else:
            question = "Alterar o Gênero para o Filme Listado?"
            objects_caption = "Filme Selecionado para Alteração de Gênero"

        #  O modelo 'admin/includes/fieldset.html' exibe os campos do formulário no mesmo formato que admin/change_form.html
        #  Fonte: https://www.dmertl.com/blog/?p=116 
        adminform = helpers.AdminForm(
            form,
            list([(None, {'fields': form.base_fields})]),
            self.get_prepopulated_fields(request))

        objects_out = "TAB_I" # utilize QS_KV, LNO_I ou TAB_I

        if objects_out == "QS_KV": # Para Lista não Ordenada com Queryset utilizando "key, value"
                                   # Registrado apenas para fins didáticos, 
                                   # pois é necessário indicar os nomes dos campos no template
            objects = queryset
        elif objects_out == "LNO_I": # Para Lista não Ordenada com List utilizando "índices"
            corpo_list = queryset.values_list('pk', 'title', 'genre__title', 'data', 'data_hora')
            objects = {'corpo_list': corpo_list,}
        else: # Para Tabela com List utilizando "índices"
            cabecalho_list = ['Título do Filme', 'Gênero', 'Data Qualquer', 'Data e Hora Qualquer']
            corpo_list = queryset.values_list('pk', 'title', 'genre__title', 'data', 'data_hora')
            objects = {'cabecalho_list': cabecalho_list, 'corpo_list': corpo_list,}

        options = {
            'title': "Atualizar Gênero de Filme",
            'question': question,
            'tot_queryset': tot_queryset,
            'objects': objects,
            'objects_out': objects_out,
            'objects_caption': objects_caption,
            'form': form,
            'adminform': adminform,
            'post_action': post_action,
            'action_name': action_name,
            'app_label': self.model._meta.app_label,
            'app': self.opts.app_label,
            'modelo': self.opts.model_name,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request),
            'has_permission': self.has_change_permission(request), # necessário para exibir {% block usertools %}
        }
        return render(request, 'admin/actions/actions_ordinary.html', options)
    set_genre_action_002.short_description = u'Atualizar Gêneros - Utilizando Update Queryset'
    set_genre_action_002.allowed_permissions = ('change', )
    # X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X 


    # Alterar status com parametro(s) fixo(s) e template exclusivo
    # Fonte: https://www.willandskill.se/en/custom-django-admin-actions-with-an-intermediate-page/
    # **********************************************
    def update_status_001_param_fixo_template_exclusivo(self, request, queryset):
        # Observe input type="submit" name="apply" no template html:
        # <input type="submit" name="apply" value="Atualizar"/>

        # Todas as requests aqui serão, na verdade, do tipo POST portanto, 
        # precisaremos verificar nossa chave especial 'apply' em vez do tipo de request atual
        if 'apply' in request.POST:
            # Observe o input type="hidden" name="action" value="update_status_001_param_fixo_template_exclusivo" 
            # com value igual ao nome desta actions no template html:
            # <input type="hidden" name="action" value="update_status_001_param_fixo_template_exclusivo" />

            # O usuário clicou em enviar no formulário intermediário.
            # Execute nossa ação de atualização:
            queryset.update(status=1)
            
            # Redirecionar, com uma mensagem informativa, para nossa view de 
            # administrador após nossa atualização ter concluído:
            self.message_user(request,
                              "Status de {} filmes alterado para 'Ativo'".format(queryset.count()))
            print(request.META.get('HTTP_REFERER'))
            print(request.get_full_path())
            return HttpResponseRedirect(request.get_full_path())
                        
        return render(request,
                      'admin/movies/movie/action_status.html',
                      context={'filmes':queryset})
    update_status_001_param_fixo_template_exclusivo.short_description = "Alterar Status com parâmetro fixo e template exclusivo"
    update_status_001_param_fixo_template_exclusivo.allowed_permissions = ('change', )


    # Alterar status com parametro(s) fixo(s) e template genérico
    # Fonte: https://www.willandskill.se/en/custom-django-admin-actions-with-an-intermediate-page/
    # **********************************************
    def update_status_002_param_fixo_template_generico(self, request, queryset):
        post_action ='do_action' 
        action_name = 'update_status_002_param_fixo_template_generico' 
        form = None
        adminform = None
        # Observe input type="submit" name="apply" no template html:
        # <input type="submit" name="apply" value="Atualizar"/>

        # Todas as requests aqui serão, na verdade, do tipo POST portanto, 
        # precisaremos verificar nossa chave especial 'apply' em vez do tipo de request atual
        if post_action in request.POST:
            # Observe o input type="hidden" name="action" value="update_status_002_param_fixo_template_generico" 
            # com value igual ao nome desta actions no template html:
            # <input type="hidden" name="action" value="update_status_002_param_fixo_template_generico" />

            # O usuário clicou em enviar no formulário intermediário.
            # Execute nossa ação de atualização:
            queryset.update(status=1)
            
            # Redirecionar, com uma mensagem informativa, para nossa view de 
            # administrador após nossa atualização ter concluído:
            self.message_user(request,
                              "Status de {} filmes alterado para 'Ativo'".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())
        
        tot_queryset = queryset.count()
        if tot_queryset > 1:
            question = "Alterar o Status para os " + str(tot_queryset) + " Filmes Listados?"
            objects_caption = "Filmes Selecionados para Alteração de Status"
        else:
            question = "Alterar o Status para o Filme Listado?"
            objects_caption = "Filme Selecionado para Alteração de Status"

        objects_out = "TAB_I" # utilize QS_KV, LNO_I ou TAB_I

        if objects_out == "QS_KV": # Para Lista não Ordenada com Queryset utilizando "key, value"
                                   # apenas para fins didáticos, 
                                   # pois é necessário indicar os nomes dos campos no template
            objects = queryset
        elif objects_out == "LNO_I": # Para Lista não Ordenada com List utilizando "índices"
            corpo_list = queryset.values_list('pk', 'title', 'genre__title', 'data', 'data_hora')
            objects = {'corpo_list': corpo_list,}
        else: # Para Tabela com List utilizando "índices"
            cabecalho_list = ['Título do Filme', 'Gênero', 'Data Qualquer', 'Data e Hora Qualquer']
            corpo_list = queryset.values_list('pk', 'title', 'genre__title', 'data', 'data_hora')
            objects = {'cabecalho_list': cabecalho_list, 'corpo_list': corpo_list,}
                        
        options = {
                    'title': "Atualizar Status de Filme",
                    'question': question,
                    'tot_queryset': tot_queryset,
                    'objects': objects,
                    'objects_out': objects_out,
                    'objects_caption': objects_caption,
                    'form': form,
                    'adminform': adminform,
                    'post_action': post_action,
                    'action_name': action_name,
                    'app_label': self.model._meta.app_label,
                    'app': self.opts.app_label,
                    'modelo': self.opts.model_name,
                    'opts': self.model._meta,
                    'has_change_permission': self.has_change_permission(request),
                    'has_permission': self.has_change_permission(request), # necessário para exibir {% block usertools %}
                    }
        return render(request,
                      'admin/actions/actions_ordinary.html',
                      options)
    update_status_002_param_fixo_template_generico.short_description = "Alterar Status com parâmetro fixo e template Genérico"
    update_status_002_param_fixo_template_generico.allowed_permissions = ('change', )


admin.site.register(Genre, GenreAdmin)   
admin.site.register(Movie, MovieAdmin)   

