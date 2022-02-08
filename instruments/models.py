# Passando parâmetros para a ação administrativa do Django
# Fonte : https://www.agiliq.com/blog/2014/08/passing-parameters-to-django-admin-action/

# carregue dados de de exemplo usando:
# python manage.py loaddata instruments/fixtures/instruments.json

from django.db import models

from datetime import date, timedelta

from django.utils import timezone
from django.utils.dateformat import format

from django.core.exceptions import ValidationError

from django.utils.html import format_html
from django.urls import reverse

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django.shortcuts import get_object_or_404

def validate_price_100_200(value):
    """ Validar Preço 
        Validar campo a partir de formulários e outras interfaces como, 
        por exemplo, actions"""
    if not value:
        value = 0
        
    if value >= 100 and value <= 200:
        return {'retorno': False, 'mensagem': u'%s não é um valor válido para preço - (validate_preço_100_200).' % value}
    elif value is None:
        return {'retorno': False, 'mensagem': u'Informe um valor para o preço - (validate_preço_100_200).'}
    else: 
        return {'retorno': True, 'mensagem': None}

def validate_price_1000(value):
    """ Validar Preço 
        Validar campo a partir de formulários e outras interfaces como, 
        por exemplo, actions"""
    if value == 1000:
        return {'retorno': False, 'mensagem': u'%s não é um valor válido para preço - (validate_preço_1000).' % value}
    elif value is None:
        return {'retorno': False, 'mensagem': u'Informe um valor para o preço - (validate_preço_1000).'}
    else: 
        return {'retorno': True, 'mensagem': None}

def validator_datax(value):
    """Garante que essa data seja = 01/01/1900 or esteja entre 01-01-1990 e 'year_ago' ano(s) atrás."""
    year_ago = 1
    today = date.today()
    one_year_ago = today.replace(year = today.year - year_ago)
    one_day = timedelta(days = 1)
    tomorrow = today + one_day
    yesterday = today - one_day
    # print(f'\namanhã: {tomorrow}\n')
    # print(f'\nontem: {yesterday}\n')
    # print(f'\n{year_ago} ano(s) atrás: {one_year_ago}\n')
    if value != date(1900, 1, 1) and not date(1990, 1, 1) <= value <= one_year_ago:
        raise ValidationError("validators ->> Data deve estar entre %s e %s" % (format(date(1990,1,1,), 'd/m/Y'), format(one_year_ago, 'd/m/Y')))

def validate_data_preco(price, data):
    """Garante que essa data seja = 01/01/1900 or esteja entre 01-01-1990 e 'year_ago' ano(s) atrás."""
    year_ago = 1
    today = date.today()
    one_year_ago = today.replace(year = today.year - year_ago)
    one_day = timedelta(days = 1)
    yesterday = today - one_day
    tomorrow = today + one_day
    
    if (data != date(1900, 1, 1) or (not date(1990, 1, 1) <= data <= one_year_ago)) and (price <= 10):
        return {'retorno': False, 'mensagem': u"Data deve estar entre %s e %s para preço %s" % (format(date(1990,1,1,), 'd/m/Y'), format(one_year_ago, 'd/m/Y'), price)}
    elif (data < yesterday or data > tomorrow ) and (price > 10):
        return {'retorno': False, 'mensagem': u"Data deve estar entre %s e %s para preço %s" % (format(yesterday, 'd/m/Y'), format(tomorrow, 'd/m/Y'), price)}
    else: 
        return {'retorno': True, 'mensagem': None}
        # raise ValidationError("Data deve estar entre %s e %s" % (format(date(1990,1,1,), 'd/m/Y'), format(one_year_ago, 'd/m/Y')))
        
class Instrument(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome do Equipamento')
    price = models.IntegerField()
    # data = models.DateField(verbose_name='data x', default=timezone.now, validators=[validator_datax])
    data = models.DateField(verbose_name='data x', default=timezone.now)

    class Meta:
        verbose_name = 'Equipamento'
        verbose_name_plural = 'Equipamentos'

    def __str__(self):
        return self.name

    def admin_unit_details(self):  # Button for admin to get to API
        link = reverse('intrument_detalhe', args=[self.pk])
        html = '<a href="{}\">Detalhe</a>'.format(link)
        # return format_html(html)   
        return format_html(u'<a href=' + link + ' onclick="return true" class="button" '
                            u'id="id_admin_unit_selected">Model Details</a>')
    # admin_unit_details.allow_tags = True
    admin_unit_details.short_description = ""

    # def clean(self):
    #     super().clean()
    #     if self.price == 1000:
    #         raise ValidationError(u'%s valor não é válido para price XX Clean.' % self.price)

    def clean(self):
        super().clean()
        price = self.price
        if not price: price = 0 
        data = self.data
        valida_price_1000 = validate_price_1000(price)
        valida_data_preco = validate_data_preco(price, data)
        if valida_price_1000["retorno"] == False:
            raise ValidationError({'price':[valida_price_1000["mensagem"]]}) # exibe a mensagem de erro acima do campo
            # raise ValidationError(valida_price_1000["mensagem"]) # exibe a mensagem de erro no topo do formulário
        if valida_data_preco["retorno"] == False:
            # raise ValidationError({'data':[valida_data_preco["mensagem"]]}) # exibe a mensagem de erro acima do campo
            raise ValidationError(valida_data_preco["mensagem"]) # exibe a mensagem de erro no topo do formulário

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        price = self.price
        valida = validate_price_100_200(price)
        if valida["retorno"] == False:
            raise ValidationError({'price':[valida["mensagem"]]}) # exibe a mensagem de erro acima do campo
            # raise ValidationError(valida["mensagem"]) # exibe a mensagem de erro no topo do formulário

@receiver(pre_save, sender=Instrument)
def other_pre_save_actions(sender, instance, *args, **kwargs):
    print('-------------')
    print('pre_save ocorreu')
    print(instance._meta.app_label)
    
    if instance.id is None:
        print('inclusao')
        print(instance.name, instance.data, instance.price)
        print(instance.pk)
    else: # Alteração
        print('Alteração')
        obj = get_object_or_404(Instrument, pk=instance.pk)
        for f in instance._meta.fields:
            print(f.attname, getattr(obj, f.attname))
    return

@receiver(post_save, sender=Instrument)
def other_pre_save_actions(sender, instance, *args, **kwargs):
    print('-------------')
    print('post_save ocorreu')
    print(instance.name, instance.data, instance.price)
    print(instance.pk)
    return