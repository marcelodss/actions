# https://docs.djangoproject.com/en/3.2/topics/forms/

from operator import truediv
from .models import (Genre, STATUS, validate_genero)
from geral.validacoes import string_to_date_naive
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets   

STATUS_TESTE = ((None, "Selecione ..."),) + STATUS[0:]
STATUS_GEEK = ((None, "Selecione o geeks field..."),) + STATUS[0:]

def validate_generoForm(value):
    """ Custom validator 
        ValidationError só funciona quando chamado dentro de formulários, portanto
        utilizamos um validador 'validate_genero' e o chamamos a partir deste.
        Assim mantemos a consistência da validação para este campo que será atualizado,
        também, a partir de outra interface, neste caso, uma action."""
    if validate_genero(value) == False:
        raise ValidationError(u'%s não é um valor válido para gênero XXX Custom validator.' % value)

class GenreFormComSave(forms.Form):
    genre = forms.ModelChoiceField(empty_label="Selecione o Gênero", required=True, label="Gênero", help_text = "O Gênero 'Mais' não deve ser usado.",
            queryset=Genre.objects.all(),
            )
    teste = forms.ChoiceField(required=False, label="Teste", choices = STATUS_TESTE,)
    geeks_field = forms.TypedChoiceField(required=False, label="GEEks field", choices = STATUS_GEEK, coerce = str)
    data_inicio = forms.DateField(required=True, widget=AdminDateWidget(), label="DT InICiO",)
    from_date = forms.DateField(widget=AdminDateWidget(), label="FROM Date",)
    mydate = forms.DateField(widget=widgets.AdminDateWidget, label="Minha Datinha",)
    mydate_format = forms.DateField(widget=widgets.AdminDateWidget(attrs={'type': 'date'}) , label="date format",)
    
    # VEJA-ME PARA DATE PICKER
    # https://qastack.com.br/programming/38601/using-django-time-date-widgets-in-custom-form 

    def clean(self):
        print('\n\nAqui....\n')
        super(GenreFormComSave, self).clean()
        print('\n\nAqui de novo....\n')
        if 'data_inicio' in self.cleaned_data: 
            print('\n\nAqui de novo no if....\n')
            data_inicio = self.cleaned_data('data_inicio')
            print('\n\nAqui de novo data inicio....\n', data_inicio)
            if string_to_date_naive(data_inicio) == None:
                print('\n\nAqui de novo no if do naive....\n')
                raise ValidationError("Data inválida.")
            else:
                print('\n\nAqui de novo no else do naive....\n')

class GenreFormComUpdate(forms.Form):
    genre = forms.ModelChoiceField(required=True, 
            empty_label="Selecione o Gênero", label="Gênero", help_text = "O Gênero 'Mais' não deve ser usado.",
            initial=None,
            queryset=Genre.objects.all(),)
    def clean_genre(self):
        genre = self.cleaned_data['genre']
        valida = validate_genero(genre)
        if valida["retorno"] == False:
            raise ValidationError(valida["mensagem"])
        return genre # Sempre retorna o dado validado, você tendo mudado ele ou não.



