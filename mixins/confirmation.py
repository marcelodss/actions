from django.template.response import TemplateResponse
from django.contrib.admin import helpers
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.options import TO_FIELD_VAR

from django.core.exceptions import PermissionDenied
from django.contrib.admin.utils import flatten_fieldsets, unquote
from django.forms.formsets import all_valid

IS_POPUP_VAR = '_popup'

class ConfirmationMixin(object):
    def changeform_view(self, request, object_id, form_url, extra_context):
        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        model = self.model
        opts = model._meta

        if request.method == 'POST' and '_saveasnew' in request.POST:
            object_id = None

        add = object_id is None

        if add:
            if not self.has_add_permission(request):
                raise PermissionDenied
            obj = None

        else:
            obj = self.get_object(request, unquote(object_id), to_field)

            if request.method == 'POST':
                if not self.has_change_permission(request, obj):
                    raise PermissionDenied
            else:
                if not self.has_view_or_change_permission(request, obj):
                    raise PermissionDenied

            if obj is None:
                return self._get_obj_does_not_exist_redirect(request, opts, object_id)

        fieldsets = self.get_fieldsets(request, obj)
        ModelForm = self.get_form(
            request, obj, change=not add, fields=flatten_fieldsets(fieldsets)
        )
        if request.method == 'POST' and request.POST.get('_confirmation') and not IS_POPUP_VAR in request.GET:
            form = ModelForm(request.POST, request.FILES, instance=obj)
            form_validated = form.is_valid()
            if form_validated:
                new_object = self.save_form(request, form, change=not add)
            else:
                new_object = form.instance
            formsets, inline_instances = self._create_formsets(request, new_object, change=not add)

                
            if all_valid(formsets) and form_validated:
                new_object = form.save(commit=False)
                # self.save_model(request, new_object, form, not add)
                # self.save_related(request, form, formsets, not add)
                # change_message = self.construct_change_message(request, form, formsets, add)
                # if add:
                #     self.log_addition(request, new_object, change_message)
                #     #return self.response_add(request, new_object)
                # else:
                #     self.log_change(request, new_object, change_message)
                #     #return self.response_change(request, new_object)
        #     else:
        #         form_validated = False
        # else:
            if add:
                # initial = self.get_changeform_initial_data(request)
                # form = ModelForm(initial=initial)
                form = ModelForm(request.POST, request.FILES, instance=obj)
                formsets, inline_instances = self._create_formsets(request, form.instance, change=False)
            else:
                form = ModelForm(instance=obj)
                formsets, inline_instances = self._create_formsets(request, obj, change=True)

            if not add and not self.has_change_permission(request, obj):
                readonly_fields = flatten_fieldsets(fieldsets)
            else:
                readonly_fields = self.get_readonly_fields(request, obj)
            adminForm = helpers.AdminForm(
                form,
                list(fieldsets),
                # Clear prepopulated fields on a view-only form to avoid a crash.
                self.get_prepopulated_fields(request, obj) if add or self.has_change_permission(request, obj) else {},
                readonly_fields,
                model_admin=self)
            media = self.media + adminForm.media

            inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
            for inline_formset in inline_formsets:
                media = media + inline_formset.media

            if add:
                title = 'Confirmar adi????o para '
                breadcrumb = 'Adiciona'
            elif self.has_change_permission(request, obj):
                title =' Confirmar altera????o para '
                breadcrumb = obj
            else:
                title = 'Consulta'
                breadcrumb = 'Consulta '

            context = {
                **self.admin_site.each_context(request),
                'title': title +  opts.verbose_name,
                'breadcrumb': breadcrumb,
                'subtitle': str(obj) if obj else None,
                'adminform': adminForm,
                'object_id': object_id,
                'original': obj,
                'is_popup': IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET,
                'to_field': to_field,
                'media': media,
                'inline_admin_formsets': inline_formsets,
                'errors': helpers.AdminErrorList(form, formsets),
                'preserved_filters': self.get_preserved_filters(request),
                'opts': self.model._meta,
                'add': add,
                'change': self.has_change_permission(request),
                'has_change_permission': self.has_change_permission(request),
                'has_add_permission': self.has_add_permission(request),
                'has_view_permission': self.has_view_permission(request),
                'save_as': self.save_as,
            }

            # Hide the "Save" and "Save and continue" buttons if "Save as New" was
            # previously chosen to prevent the interface from getting confusing.
            if request.method == 'POST' and not form_validated and "_saveasnew" in request.POST:
                context['show_save'] = False
                context['show_save_and_continue'] = False
                # Use the change template instead of the add template.
                add = False

            context.update(extra_context or {})
            return TemplateResponse(
                request, 'admin/confirma_submit/form_confirmation.html', context)
            # if request.POST.get('_confirmation'):
            #     return self.render_change_form(request, context, add=add, change=not add, obj=obj, form_url=form_url)
            
        return super().changeform_view(request, object_id, form_url, extra_context)


