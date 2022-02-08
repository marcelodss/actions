from django.urls import path
# from django.contrib import admin

from .admin import InstrumentAdmin as intrument_detalhe


urlpatterns = [
    path('instruments/instrument/<int:pk>/detalhe/', intrument_detalhe.detalhe, name='intrument_detalhe'),
]

