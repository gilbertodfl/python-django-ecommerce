from django.urls import path
from .views import *

"""
Resumindo os três parâmetros do path():

1º '' → o padrão da URL
2º homepage → a view que processa a requisição
3º name="homepage" → um apelido para referenciar essa URL no código (ex: reverse('homepage') ou {% url 'homepage' %} nos templates)
"""

urlpatterns = [
    path('', homepage, name="homepage"),
    path('loja/', loja, name="loja"),
    path('loja/<str:filtro>/', loja, name="loja"),
    path('produto/<int:id_produto>/', ver_produto, name="ver_produto"),
    path('produto/<int:id_produto>/<int:id_cor>/', ver_produto, name="ver_produto"),
    path('carrinho/', carrinho, name="carrinho"),
    path('checkout/', checkout, name="checkout"),
    path('adicionar_carrinho/<int:id_produto>/', adicionar_carrinho, name="adicionar_carrinho"),
    path('remover_carrinho/<int:id_produto>/', remover_carrinho, name="remover_carrinho"),
    path('adicionar_endereco', adicionar_endereco, name="adicionar_endereco"),
    path('minhaconta/', minha_conta, name="minha_conta"),
    path('login/', fazer_login, name="fazer_login"),
    path('logout/', fazer_logout, name="fazer_logout"),    
    path('criarconta/', criar_conta, name="criar_conta"),

]