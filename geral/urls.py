
from django.urls import path

from .views import home, teste01, teste02
from .views import view_para_template
from .views import CBV_TemplateView001
from .views import CBV_View001
from .views import validate_nomNro

urlpatterns = [
    path('', home, {'extra': 'home com contexto extra na url'}, name = 'home'),
    path('teste01/<int:parametro>/', teste01, {'extra': 'teste (mesma view) com parâmentro e contexto extra'}, name='teste01_com_parametro'),
    path('teste01/', teste01, {'extra': 'teste (mesma view) sem parâmentro e contexto extra'}, name='teste01_sem_parametro'),
    path('teste02/', teste02, name='teste02'),  # exemplo: /teste02/?dia=domingo&mapa=brasil
    path('view_para_template/', view_para_template, name='view_para_template'), 
    path('cbv_template_view_001/', CBV_TemplateView001.as_view (), {'dados_url':True}, name='cbv_template_view_001'), 
    path('cbv_view_001/', CBV_View001.as_view (), name='cbv_view_001'), 
    path('ajax/', validate_nomNro, name='ajax_validade'),
]
