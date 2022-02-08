from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

from django.core.exceptions import PermissionDenied

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json
from django.utils.translation import gettext
from django.utils.text import get_text_list
from urllib.parse import unquote, quote

from django.urls import reverse

def format_change_message(obj):
    """
    Se self.change_message é uma estrutura JSON, interpretá-la como uma 
    string, tradicionalmente traduzido.
    """
    if obj and obj[0] == '[':
        try:
            change_message = json.loads(obj)
        except json.JSONDecodeError:
            return obj
        messages = []
        for sub_message in change_message:
            if 'added' in sub_message:
                if sub_message['added']:
                    sub_message['added']['name'] = gettext(sub_message['added']['name'])
                    messages.append(gettext('Added {name} “{object}”.').format(**sub_message['added']))
                else:
                    messages.append(gettext('Added.'))

            elif 'changed' in sub_message:
                sub_message['changed']['fields'] = get_text_list(
                    [gettext(field_name) for field_name in sub_message['changed']['fields']], gettext('and')
                )
                if 'name' in sub_message['changed']:
                    sub_message['changed']['name'] = gettext(sub_message['changed']['name'])
                    messages.append(gettext('Changed {fields} for {name} “{object}”.').format(
                        **sub_message['changed']
                    ))
                else:
                    messages.append(gettext('Changed {fields}.').format(**sub_message['changed']))

            elif 'deleted' in sub_message:
                sub_message['deleted']['name'] = gettext(sub_message['deleted']['name'])
                messages.append(gettext('Deleted {name} “{object}”.').format(**sub_message['deleted']))

        change_message = ' '.join(msg[0].upper() + msg[1:] for msg in messages)
        return change_message or gettext('No fields changed.')
    else:
        return obj

def custom_history(request, extra=None):
    if not request.user.is_authenticated:
        messages.warning(request,'Login necessário.')
        return redirect(f"{reverse('admin:login')}?next={quote(request.get_full_path())}")
    elif not request.user.is_staff:
        messages.warning(request,'Acesso disponível apenas para membros de equipe.')
        return redirect(f"{reverse('admin:index')}")

    template = 'admin/object_history_custom.html'

    app_for_history = None
    model_for_history = None
    ct_for_history = None
    opts_for_history = request.GET.get(unquote('opts'), None)
    parameter_pk = request.GET.get(unquote('pk'), None)
    user_for_history = None
    user_has_perm_for_history = False
    obj = None
    app_label = None
    model_label = None
    model_label_plural = None
    has_permission = False

    logs = None
    logCount = 0

    if opts_for_history:
        opts_for_history = opts_for_history.split('.')

    if type(opts_for_history) is list and len(opts_for_history) == 2:
        if type(opts_for_history[0]) is str and type(opts_for_history[1]) is str:
            app_for_history = opts_for_history[0]
            model_for_history = opts_for_history[1]
        else:
            return render(request, 'admin/404.html')
    else:
        return render(request, 'admin/404.html')

    if app_for_history and model_for_history and parameter_pk:
        try:
            ct_for_history =  ContentType.objects.get(app_label=app_for_history, model=model_for_history)
        except:
            return render(request, 'admin/404.html')

    if ct_for_history and parameter_pk:
        if request.user.pk:
            from django.contrib.auth import get_user_model
            User_for_history = get_user_model()
            user_for_history = User_for_history.objects.get(pk=request.user.pk)
 
            if user_for_history.is_superuser and user_for_history.is_active:
                user_has_perm_for_history = True
            elif user_for_history.has_perm(f'{app_for_history}.view_{model_for_history}'):
                user_has_perm_for_history = True
            elif user_for_history.has_perm(f'{app_for_history}.change_{model_for_history}'):
                user_has_perm_for_history = True

    if user_has_perm_for_history == False:
        raise PermissionDenied()
    else:
        has_permission = True

    if ct_for_history and parameter_pk:
        try:
            obj = ct_for_history.get_object_for_this_type(pk=parameter_pk)
        except:
            obj = None

        if ct_for_history.id:
            # logs = LogEntry.objects.filter(
            #     content_type_id=ct_for_history.id, object_id=parameter_pk).order_by('-id')[:100]
            logs = LogEntry.objects.filter(
                content_type_id=ct_for_history.id, object_id=parameter_pk).order_by('-id')
  

            history_format = []

            for log in logs:
                history_format.append((log.action_time, log.user, format_change_message(log.change_message)))

            page = request.GET.get('pg', 1)
            page_itens = 30
            paginator = Paginator(history_format, page_itens)
            page_range = paginator.get_elided_page_range(number=page, on_each_side=4 , on_ends=2)
        try:
            log_history = paginator.page(page)
        except PageNotAnInteger:
            log_history = paginator.page(1)
        except EmptyPage:
            log_history = paginator.page(paginator.num_pages)

    if logs:
        if logs.exists(): 
            logCount = logs.count()

    if obj:
        if obj._meta.app_config.verbose_name:
            app_label = obj._meta.app_config.verbose_name
        elif obj._meta.app_label:
            app_label = obj._meta.app_label.replace('_', ' ').capitalize()
        else:
            app_label = app_for_history.replace('_', ' ').capitalize()
        
        if obj._meta.verbose_name:
            model_label = obj._meta.verbose_name
        else:
            model_label = model_for_history.replace('_', ' ').capitalize()
        
        if obj._meta.verbose_name_plural:
            model_label_plural = obj._meta.verbose_name_plural
        else:
            model_label_plural = model_for_history.replace('_', ' ').capitalize()
        
    else:
        app_label = app_for_history.replace('_', ' ').capitalize()
        model_label = model_for_history.replace('_', ' ').capitalize()
        model_label_plural = model_for_history.replace('_', ' ').capitalize()

    change_list_url = reverse('admin:' + app_for_history + '_' + model_for_history + '_changelist')
    change_url = reverse('admin:' + app_for_history + '_' + model_for_history + '_change', args=(parameter_pk,))

    user = request.user

    return render(request, template, {
        'opts': opts_for_history[0] + '.' + opts_for_history[1],
        'pk': parameter_pk,
        'obj': obj,
        'app_label': app_label,
        'app_name': opts_for_history[0],
        "model_label":model_label, 
        "model_label_plural":model_label_plural, 
        'change_list_url': change_list_url,
        'change_url': change_url,
        "logCount":logCount,
        "log_history": log_history,
        "page_range": page_range,
        "page_itens": page_itens,
        'user': user,
        'has_permission': has_permission,
        'is_blank': 1,
        'site_header': admin.site.site_header,
        'site_title': admin.site.site_title,
        'title': 'Histórico de Cadastros',
        'subtitle': app_label  + ' - ' + model_label_plural,
     })
     