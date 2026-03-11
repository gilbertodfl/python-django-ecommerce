from django.shortcuts import render, redirect
from django.template import context
from  .models import * 
import uuid 
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
        id_cor = dados.get('id_cor')
        if not tamanho:
            return redirect('ver_produto', id_produto=id_produto)
        print("Adicionar ao carrinho: Produto ID:", id_produto)
        
        if not id_cor or not tamanho:
            return redirect('ver_produto', id_produto=id_produto)
        if request.user.is_authenticated:   
            print('entrei no authenticated')
            cliente = request.user.cliente
            pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
            item_estoque = ItemEstoque.objects.get(produto__id=id_produto, cor__id=id_cor, tamanho=tamanho)
            print( pedido)
            if item_estoque and item_estoque.quantidade > 0:
                print('entrei no if do item_estoque')

                itens_pedido, criado = ItensPedido.objects.get_or_create(pedido=pedido, item_estoque=item_estoque)
                if not criado:
                    itens_pedido.quantidade += 1
                    print('Produto já no carrinho, incrementando quantidade para:', itens_pedido.quantidade)
                else:
                    print('novo item no pedido')
                    itens_pedido.quantidade = 1
                itens_pedido.save()
                item_estoque.quantidade -= 1
                item_estoque.save()
        else:
            ## aqui vamos gerar um id de sessão para o usuário não autenticado, e armazenar os itens do carrinho em uma 
            # estrutura de dados associada a esse id de sessão.
            if request.COOKIES.get('id_sessao'):
                id_sessao = request.COOKIES.get('id_sessao')
            else:
                id_sessao = str(uuid.uuid4())
            resposta = redirect('loja')
            resposta.set_cookie(key='id_sessao',value=id_sessao, max_age=30*24*60*60)  # Cookie válido por 30 dias
            return resposta

        return redirect('carrinho')
    else:
        return redirect('loja')
    
def remover_carrinho(request, id_produto):
    if request.method == 'POST' and  id_produto:
        dados = request.POST.dict()
        tamanho = dados.get('tamanho')
        id_cor = dados.get('id_cor')
        if not tamanho:
            return redirect('ver_produto', id_produto=id_produto)
        print("Adicionar ao carrinho: Produto ID:", id_produto)
        
        if not id_cor or not tamanho:
            return redirect('ver_produto', id_produto=id_produto)
        if request.user.is_authenticated:   
            cliente = request.user.cliente
            pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
            item_estoque = ItemEstoque.objects.get(produto__id=id_produto, cor__id=id_cor, tamanho=tamanho)
            item_pedido, criado = ItensPedido.objects.get_or_create(pedido=pedido, item_estoque=item_estoque)
            item_pedido.quantidade -= 1
            item_estoque.quantidade += 1   
            item_pedido.save()
            if item_pedido.quantidade <= 0:
                item_pedido.delete()
            
        else:
            return redirect('loja')

        return redirect('carrinho')
    else:
        return redirect('loja')
def carrinho(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        itens_pedido = ItensPedido.objects.filter(pedido=pedido)
        context = { 'itens_pedido': itens_pedido , 'pedido': pedido}
    else:
        context = { 'itens_pedido': [] }    
    return render(request, 'carrinho.html', context)    

def checkout(request):
    return render(request, 'checkout.html')


def minha_conta(request):
    return render(request, 'usuario/minha_conta.html')

def login(request):
    return render(request, 'usuario/login.html')