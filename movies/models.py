# Passando parâmetros para a ação administrativa do Django
# fonte: https://en.proft.me/2015/01/29/admin-actions-django-custom-form/

# carregue dados exemplo com:
# python manage.py loaddata movies/fixtures/movies.json


# from django.contrib.messages.api import error
from django.db import models
from django.utils import timezone

# from django.core import validators
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

# Create your models here.
STATUS = (
    (1, 'Ativo'), 
    (2, 'Inativo'), 
)

def validate_score(value):
    """ Custom validator """
    if not value:
        value = 0
        
    if value >= 100 and value <=150:
        raise ValidationError(u'%s valor não é válido para score XXX Custom validator.' % value)

def validate_genero(value):
    """ Validar Gênero 
        Validar campo a partir de formulários e outras interfaces como, 
        por exemplo, actions"""
    if value.pk in (1, 10, 99): return {'retorno': False, 'mensagem': u'%s não é um valor válido para gênero - (validate_genero).' % value}
    else: return {'retorno': True, 'mensagem': None}

class Genre(models.Model):
    title = models.CharField(u'Title', max_length=100)
    data = models.DateField(verbose_name='alguma data ', default=timezone.now)
    new_score = models.IntegerField(u'Score', validators=[validate_score], default=0)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='set_usuario', verbose_name=u'Usuário', default=1)

    # usuario = models.ManyToManyField(User, related_name='set_usuario')

    def __str__(self):
        return self.title

class Movie(models.Model):
    title = models.CharField(u'Title', max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, verbose_name=u'Genre',)
    score = models.IntegerField(u'Score', validators=[validate_score])
    status = models.IntegerField(choices=STATUS, verbose_name="Status", default=1)
    data = models.DateField(verbose_name='data x', default=timezone.now)
    hora = models.TimeField(verbose_name='hora x', default=timezone.now)
    data_hora = models.DateTimeField(verbose_name='data hora x', default=timezone.now)

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.score == 0 or self.score >= 1000:
            raise ValidationError(u'%s valor não é válido para score XX Clean.' % self.score)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        genre = self.genre
        valida = validate_genero(genre)
        if valida["retorno"] == False:
            raise ValidationError(valida["mensagem"])

    