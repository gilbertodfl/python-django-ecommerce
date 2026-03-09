from django.shortcuts import render, redirect
from django.template import context
from  .models import * 
# Create your views here.
def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    context = {
        'banners': banners
    }
    return render(request, 'homepage.html', context)

def loja(request, nome_categoria=None):
    
    if nome_categoria:
        categoria= Categoria
        ## Aqui ele consegue fazer o joiner e o filtro porque estamos usando __ e o proprio nome 
        ## mais detalhes veja no .models
        produtos = produtos.filter(categoria__nome=nome_categoria,ativo=True)
    else:
        produtos = Produto.objects.filter(ativo=True)
    
    context={
        'produtos': produtos
    }
    return render(request, 'loja.html', context)
def ver_produto(request, id_produto, id_cor=None):
    tem_estoque = False
    cores = {}
    tamanhos = {}
    cor_selecionada = None
    if id_cor:
        cor_selecionada = Cor.objects.get(id=id_cor)

    produto = Produto.objects.get(id=id_produto)
    itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0)
    # if(not itens_estoque.exists()):
    #     return render(request, 'produto_indisponivel.html')
    if len(itens_estoque) > 0:
        tem_estoque = True
        cores = { item.cor for item in itens_estoque}
        if id_cor:
            itens_estoque = itens_estoque.filter(produto=produto, quantidade__gt=0,cor__id=id_cor)
            tamanhos = { item.tamanho for item in itens_estoque}
    context = {
        'produto': produto,
        'tem_estoque': tem_estoque,
        'cores': cores,
        'tamanhos': tamanhos,
        'cor_selecionada': cor_selecionada

    }   
    return render(request, 'ver_produto.html', context)

def adicionar_carrinho(request, id_produto):
    if request.method == 'POST' and  id_produto:
        dados = request.POST.dict()
        tamanho = dados.get('tamanho')
        print(dados)
        if not tamanho:
            return redirect('ver_produto', id_produto=id_produto)
        print("Adicionar ao carrinho: Produto ID:", id_produto)
        return redirect('carrinho')
    else:
        return redirect('loja')
    


def carrinho(request):
    return render(request, 'carrinho.html')

def checkout(request):
    return render(request, 'checkout.html')


def minha_conta(request):
    return render(request, 'usuario/minha_conta.html')

def login(request):
    return render(request, 'usuario/login.html')