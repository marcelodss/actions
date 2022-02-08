from django import forms
from django.utils.safestring import mark_safe

class Calculadora:
    def soma(self, a, b):
        return a + b

    def subtrai(self, a, b):
        return a - b

    def multiplica(self, a, b):
        return a * b

    def divide(self, a, b):
        return a / b

class Varios:
    nro = 123

    def teste_00(self):
        return 'Teste Class'

    def teste_01(self):
        retorno = {'nro': self.nro, 'teste_00': self.teste_00()}
        return retorno

    def teste_02(self, a, b):
        c = Calculadora()
        s = c.soma(a, b)
        retorno = {'nro': self.nro, 'teste_00': self.teste_00(), 'soma': s}
        return retorno
   
class SearchWhileClean:
    def search_in_shop(self, args):
        msg = None
        shop = None
        if 'shop' in args['fields_keys_values']:
            shop = args['fields_keys_values']['shop'].name

        if shop:
            from confirm.models import Shop
            exist_shop = Shop.objects.filter(name__iexact=shop)
            tot_shop = 0
            if exist_shop.exists():
                tot_shop=exist_shop.count()
            if tot_shop > 0:
                msg = '- existem outros (> 0) ' + str(shop)
            if tot_shop > 1:
                msg = msg + '<br>- existem outros (> 1) ' + str(shop) + ': ' + str(tot_shop)
        return msg 

def add_confirm_field_to_admin_form(my_model):
    """
    Adiciona um campo 'hidden' (não vinculado ao Modelo de Dados) ao ModelForm 
    do Django Admin. O campo será tornado visível como um 'checkbox' que
    será utilizando em conjunto com o método clean(), permitindo confirmar as 
    'inconsistências opcionais'

    Chamada: 
    - from mixins.confirmation_field_to_admin_form import add_confirm_field_to_admin_form
    - form = add_confirm_field_to_admin_form(<model_name>)
    """
    class ConfirmFieldToAdminForm(forms.ModelForm):
        CONFIRMATION_LABEL = 'Marque este campo para confirmar o(s) alerta(s) em azul. Após, reenvie os dados.'
        CONFIRMATION_MSG = {}
        confirmation_field = forms.BooleanField(widget=forms.HiddenInput, initial=False, required=False, label="")
        
        class Meta:
            model = my_model
            form_fields_editables = {field.name: field.editable for field in my_model._meta.fields}
            form_fields = [k for k, v in form_fields_editables.items() if v == True]
            form_fields.insert(0, 'confirmation_field') 
            fields = form_fields
        
        def clean(self):
            super().clean()
            if 'confirmation_field' in self.cleaned_data and not self.cleaned_data['confirmation_field']:
                app_label = my_model._meta.app_label
                model_name = my_model._meta.model_name
                fields_names = self.fields
                
                pk = 0
                if self.instance.pk:
                    pk = self.instance.pk

                readonly_values = {}
                if self._meta.exclude:
                    for read_only_field in self._meta.exclude:
                        readonly_values[read_only_field] = getattr(self.instance, read_only_field)

                fields_keys_values = {}
                for key, value in readonly_values.items():
                    fields_keys_values[key] = value
                for field_name in fields_names:
                    if field_name in self.cleaned_data:
                        fields_keys_values[field_name] = self.cleaned_data[field_name]

                args = {}
                if fields_keys_values:
                    args = {
                        'app_label': app_label,
                        'model_name': model_name,
                        'pk': pk,
                        'fields_names': fields_names,
                        'fields_keys_values': fields_keys_values,
                    }

                if args:    
                    s = SearchWhileClean()
                    invalid_shop = s.search_in_shop(args=args)
                    if invalid_shop:
                        self.CONFIRMATION_MSG[0] = mark_safe('<span style="color:blue">' + invalid_shop + '</span>')
                        self.add_error(None, forms.ValidationError(self.CONFIRMATION_MSG[0]))

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['confirmation_field'].widget.attrs.update({"reconfirm_flag": "yes"})
            """
            Cria o atributo 'reconfirm_flag' igual a 'yes' que é utilizando com 
            'js/adm_confirmation_field_to_admin_form.js'. Este seta o valor do campo 
            'confirmation_field' para 'False' e garante que o mesmo seja recarregado
            quando ocorrerem mudanças em outros campos antes de um submit,
            mesmo já tendo sido utilizado.
            """
            confirm_set = set(self.CONFIRMATION_MSG.values())
            if confirm_set.intersection(self.non_field_errors()):
                self.fields['confirmation_field'].widget = forms.CheckboxInput()
                self.fields['confirmation_field'].label = self.CONFIRMATION_LABEL
   
    return ConfirmFieldToAdminForm