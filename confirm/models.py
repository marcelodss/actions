from django.db import models

from django.utils import timezone
from datetime import date

from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db.models.aggregates import Sum
from django.db import models
from .constants import VALID_CURRENCIES
from .validators import validate_currency

# Create your models here.

# carregue dados de de exemplo usando:
# python manage.py loaddata confirm/fixtures/itens.json

CHOICE_S_N = (
    ('S', "Sim"),
    ('N', "Não"),
)

class Item(models.Model):
    # Porque eu sou preguiçoso e não quero atualizar todas as referências de teste
    VALID_CURRENCIES = VALID_CURRENCIES

    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(max_length=3, choices=VALID_CURRENCIES)
    image = models.ImageField(upload_to="tmp/items", null=True, blank=True)
    file = models.FileField(upload_to="tmp/files", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Desconto(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='desconto_item_set', verbose_name='Item')
    item_dois = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='descontoitem_dois_set', verbose_name='Item dois', null=True, blank=True)
    descricao = models.CharField(max_length=120, verbose_name='Descrição')
    percentual = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Percentual de Desconto')
    cupom = models.CharField(max_length=3, choices=CHOICE_S_N)
    validade = models.DateField(default=timezone.now,)
    no_cartao = models.CharField(max_length=3, choices=CHOICE_S_N, null=True, blank=True)

    def __str__(self):
        return str(self.item) + " - " + self.descricao

    def clean(self):
        super().clean()
        if not self.item_dois:
            raise ValidationError("Item dois é necessário.")
        if self.validade <= date.today():
            raise ValidationError("Validade deve ser maior que hoje.")
    

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        cupom = self.cupom
        percentual = 0 
        if self.percentual: percentual = self.percentual
        if cupom == "S" and percentual >= 10:
            raise ValidationError("Para cupom S, percentual deve ser menor que 10.")

class Shop(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return str(self.name)


class Inventory(models.Model):
    class Meta:
        unique_together = ["shop", "item"]
        ordering = ["shop", "item__name"]
        verbose_name_plural = "Inventory"

    shop = models.ForeignKey(
        to=Shop, on_delete=models.CASCADE, related_name="inventory"
    )
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True, unique=True)
    notes = models.TextField(default="This is the default", null=True, blank=True)

    def __str__(self):
        return str(self.shop) + ";  " + str(self.item) 

    def clean(self):
        super().clean()
        if not self.quantity or self.quantity == 0:
            raise ValidationError("Quantidade deve ser maior que zero e não nulo.")


class GeneralManager(models.Model):
    name = models.CharField(max_length=120)
    headshot = models.ImageField(upload_to="tmp/gm/headshots", null=True, blank=True)

    def __str__(self):
        return "Diretor Geral: "+ str(self.name) 


class Town(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return str(self.name) 


class ShoppingMall(models.Model):
    name = models.CharField(max_length=120)
    shops = models.ManyToManyField(Shop, blank=True)
    general_manager = models.OneToOneField(
        GeneralManager, on_delete=models.CASCADE, null=True, blank=True
    )
    town = models.ForeignKey(Town, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "Centro de Compras: " + str(self.name)


class Transaction(models.Model):
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=VALID_CURRENCIES)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_created=True)
    date = models.DateField()

    def __str__(self):
        return  str(self.total) + ": " + str(self.currency) + "; " + str(self.shop) 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ItemSale(models.Model):
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="item_sales"
    )
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(max_length=5, validators=[validate_currency])
    desconto = models.ForeignKey(Desconto, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return  str(self.transaction) + ": " + str(self.item) + "; " + str(self.quantity) 


    def clean(self):
        errors = {}
        # check that shop has the stock
        shop = self.transaction.shop
        inventory = Inventory.objects.filter(shop=shop, item=self.item)
        if not inventory:
            errors["item"] = "Loja não tem o item abastecido"
        else:
            in_stock = inventory.aggregate(Sum("quantity")).get("quantity__sum", 0)
            if in_stock < self.quantity:
                errors["item"] = "Loja não tem o suficiente do item abastecido"
        if errors:
            raise ValidationError(errors)


class Checkout(Transaction):
    """
    Modelo Proxy para usar no Django Admin para criar uma transação
    Como se um cliente fosse verificando em um checkout físico
    """

    class Meta:
        proxy = True

