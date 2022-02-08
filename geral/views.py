from django import http

from django.http import JsonResponse
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from random import *

# from aplicacoes.cargos_em_comissao_antigo.models import Documentos

def home(request, extra=None):
    valor_1 = 1
    valor_2 = 20
    res ={'multiplicacao': valor_1 * valor_2, 'extra': extra}
    usuario = 'marcelo'
    if not User.objects.filter(username__iexact=usuario):
        print(f'{usuario} não existe')
        User.objects.create_superuser(username = usuario,
                                email='marcelo.dss@gmail.com',
                                password=randint(100,1000))
    return render(request, 'home.html', {'result': res})
    

# https://www.webforefront.com/django/accessurlparamstemplates.html?
def teste01(request, parametro=0, extra=None):
    res ={'multiplicacao': parametro * 2, 'extra': extra}
    return render(request, 'teste01.html', {'result': res})

""" 
Método de visualização do Django extraindo parâmetros de url com request.GET
https://www.webforefront.com/django/accessurlparamstemplates.html?
"""
def teste02(request, parametro_id=0, local=None):
    # Extraia o valor 'dia' ou 'mapa' anexado ao url, 
    # por exemplo: http://10.49.22.141:8080/teste02/?dia=domingo&mapa=brasil
    dia = request.GET.get('dia', '')
    mapa = request.GET.get('mapa', '')
    res ={'dia': dia, 'mapa': mapa}
    # 'dia' tem o valor 'domingo' ou '' se o dia não estiver no url
    # 'mapa' tem o valor 'brasil' ou '' se o mapa não estiver no url
    print(dia)
    print(mapa)
    return render(request,'teste02.html', {'result': res})

# https://www.webforefront.com/django/viewmethodrequests.html?
def view_para_template(request, store_id = 1, location = None): 
    # Métodos Request
    # Criar estruturas de dados fixas para passar para o template. 
    # dados podem vir de consultas de banco de dados, 
    # serviços web ou APIs sociais. 
    STORE_NAME = 'Downtown' 
    store_address = {'street': 'Main # 385', 'city': 'San Diego', 'state': 'CA'} 
    store_amenities = ['WiFi', 'A / C'] 
    store_menu = ((0, '') , (1, 'Drinks'), (2, 'Food')) 
    values_for_template = {'store_name': STORE_NAME, 'store_address': store_address, 
                           'store_amenities': store_amenities, 'store_menu':store_menu} 
    return render (request, 'viewParaTemplate.html', values_for_template)

"""
Listagem 2-37 CBV herdada de TemplateView com definição de url
https://www.webforefront.com/django/classbasedviews.html?
"""
from django.views.generic import TemplateView
class CBV_TemplateView001(TemplateView):
      template_name = 'cbvTemplateView001.html'

      def get_context_data(self, **kwargs):
        # ** kwargs contém valores de inicialização de contexto de palavra-chave (se houver) 
        # Call implementação de base para obter um contexto
        context = super(CBV_TemplateView001, self).get_context_data(**kwargs)
        print(kwargs)
        # Adicionar dados de contexto para passar para o template
        context['aboutdata'] = 'Zé da Silva'
        return context

"""
Listagem 2-38 CBV herdada de View com manipulação múltipla de HTTP
https://www.webforefront.com/django/classbasedviews.html?
"""
from django.views.generic import View 
from django.http import HttpResponse, request 

class CBV_View001 (View): 
    mytemplate = 'cbvView001.html' 
    unsupported = 'Operação não suportada - Cliquei em Post' 

    def get (self, request): 
        print(f'\n{request}\n{self.mytemplate}\n')
        context = 123
        return render(request, self.mytemplate) 
    
    def post (self, request): 
        print(f'\n{self.unsupported}')
        return HttpResponse (self.unsupported) 


@login_required
def validate_nomNro(request):
    nomNro = request.GET.get('nomNro', None)
    pk = request.GET.get('id_pk_do_modelo', None)
    if not pk:
        pk = '0'
    print(pk)
    data = {
        # 'is_taken': Documentos.objects.filter(nomNro__iexact=nomNro).exists()
        # 'is_taken': Documentos.objects.filter(nomNro__iexact=nomNro).exists()
        'is_taken': "Teste"
    }
    print(data)
    return JsonResponse(data)



