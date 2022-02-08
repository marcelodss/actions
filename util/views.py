from django.shortcuts import render, redirect

# from django.http import HttpResponse
# ...
# def teste(request):
#     return HttpResponse("Página Carregada...")

# Create your views here.

from movies.models import Movie
from confirm.models import Desconto
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime

from urllib.parse import quote
from django.urls import reverse


@login_required
def teste(request):

    pk = request.GET.get('pk_model', None)
    data = request.GET.get('data', None)
    score = request.GET.get('score', None)
    status = request.GET.get('status', None)
    title = request.GET.get('title', None)
    
    item = request.GET.get('item', None)

     
    if not pk: pk = '0'
    if data: data = datetime.strptime(data, '%d/%m/%Y')

    erro = 'N'

    if Movie.objects.filter(title__iexact=title).exists() == True:
        erro = 'Detalhe já Cadastrado'

    if Desconto.objects.filter(item__id__iexact=item).exists() == True:
        erro = 'Item já existe'

    data = {
        'erro': erro
    }

    return JsonResponse(data)
    

