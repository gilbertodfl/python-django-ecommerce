from math import prod
from django.shortcuts import render, redirect
from django.template import context
from  .models import * 
import uuid 
from .utils import filtrar_produtos, ordernar_produtos
from django.contrib.auth import authenticate, login , logout 
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your views here.
def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    context = {
        'banners': banners
    }
    return render(request, 'homepage.html', context)

def loja(request, filtro=None):

    ## pego todos os produtos ativos
    produtos = Produto.objects.filter(ativo=True)    
    ## baseado no que peguei, aplico o filtro. 
    # O filtro pode ser por categoria ou por tipo neste versão
    produtos = filtrar_produtos(produtos, filtro)

    if request.method == 'POST':
        dados = request.POST.dict()
        print(dados)
        produtos = produtos.filter(preco__gte=dados.get('preco_minimo', 0), preco__lte=dados.get('preco_maximo', 10000))
        if "tamanho" in dados:
            itens = ItemEstoque.objects.filter(produto__in=produtos, quantidade__gt=0, tamanho=dados.get("tamanho"))
            ids_produtos = itens.values_list('produto__id', flat=True).distinct()
            produtos=produtos.filter(id__in=ids_produtos)
        if "tipo" in dados:
            produtos = produtos.filter(tipo__slug=dados.get("tipo"))
        if "categoria" in dados:
            produtos = produtos.filter(categoria__slug=dados.get("categoria"))
    itens = ItemEstoque.objects.filter(produto__in=produtos, quantidade__gt=0)  
    tamanhos = itens.values_list('tamanho', flat=True).distinct()
    ids_categorias = produtos.values_list('categoria__id', flat=True).distinct()
    categorias=Categoria.objects.filter(id__in=ids_categorias)
    ##minimo, maximo= preco_minimo_maximo(produtos)
    ordem = request.GET.get("ordem","menor-preco")
    produtos = ordernar_produtos(produtos, ordem)
    context = {
        'produtos': produtos,
        'minimo': Produto.objects.order_by('preco').first().preco if produtos else 0,
        'maximo': Produto.objects.order_by('-preco').first().preco if produtos else 1000,
        'tamanhos': tamanhos,
        'categorias': categorias
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
        ##print("Adicionar ao carrinho: Produto ID:", id_produto)
        
        if not id_cor or not tamanho:
            return redirect('ver_produto', id_produto=id_produto)
        if request.user.is_authenticated:   
            ##print( 'usuario autenticado:', request.user)
            cliente = request.user.cliente
        else:
            ## aqui vamos gerar um id de sessão para o usuário não autenticado, e armazenar os itens do carrinho em uma 
            # estrutura de dados associada a esse id de sessão.
            print( 'usuario sem autenticação')
            if request.COOKIES.get('id_sessao'):
                id_sessao = request.COOKIES.get('id_sessao')
                print( 'usuario tem id_sessao:', id_sessao)
            else:
                id_sessao = str(uuid.uuid4())
                print( 'criando id_sessao:', id_sessao)
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            cliente.save()
            resposta = redirect('loja')
            resposta.set_cookie(key='id_sessao',value=id_sessao, max_age=30*24*60*60)  # Cookie válido por 30 dias
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, cor__id=id_cor, tamanho=tamanho)
        ##print( pedido)
        if item_estoque and item_estoque.quantidade > 0:
            ##print('entrei no if do item_estoque')

            itens_pedido, criado = ItensPedido.objects.get_or_create(pedido=pedido, item_estoque=item_estoque)
            if not criado:
                itens_pedido.quantidade += 1
                print('Produto já no carrinho, incrementando quantidade para:', itens_pedido.quantidade)
            else:
                print('novo item no pedido')
                itens_pedido.quantidade = 1
            itens_pedido.save()
            ##item_estoque.quantidade -= 1
            item_estoque.save()
        return resposta
    else:
        return redirect('loja')
    
def remover_carrinho(request, id_produto):
    if request.method == 'POST' and  id_produto:
        dados = request.POST.dict()
        tamanho = dados.get('tamanho')
        id_cor = dados.get('id_cor')
        if request.user.is_authenticated:   
            cliente = request.user.cliente
          
        else:
            if request.COOKIES.get('id_sessao'):
                id_sessao = request.COOKIES.get('id_sessao')
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                return redirect('loja')

        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, cor__id=id_cor, tamanho=tamanho)
        item_pedido, criado = ItensPedido.objects.get_or_create(pedido=pedido, item_estoque=item_estoque)
        item_pedido.quantidade -= 1
        ##item_estoque.quantidade += 1   
        item_pedido.save()
        if item_pedido.quantidade <= 0:
                item_pedido.delete()

        return redirect('carrinho')
    else:
        return redirect('loja')
def carrinho(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get('id_sessao'):
            id_sessao = request.COOKIES.get('id_sessao')
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            context = {"cliente_existente": False,  'itens_pedido': None , 'pedido': None}
            return render(request, 'carrinho.html', context)
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)
    context = { 'itens_pedido': itens_pedido , 'pedido': pedido, 'cliente_existente': True}

    return render(request, 'carrinho.html', context)    

def checkout(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get('id_sessao'):
            id_sessao = request.COOKIES.get('id_sessao')
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            return redirect('loja')
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    enderecos = Endereco.objects.filter(cliente=cliente)
    context = {  'pedido': pedido, 'enderecos': enderecos}

    return render(request, 'checkout.html', context)
def adicionar_endereco(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get('id_sessao'):
                id_sessao = request.COOKIES.get('id_sessao')
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                return redirect('loja')
        dados = request.POST.dict()
        rua = dados.get('rua')
        numero = dados.get('numero')
        complemento = dados.get('complemento')
        cep = dados.get('cep')
        cidade = dados.get('cidade')
        estado = dados.get('estado')

        endereco = Endereco.objects.create(
            cliente=cliente,
            rua=rua,
            numero=numero,
            complemento=complemento,
            cep=cep,
            cidade=cidade,
            estado=estado
        )
        endereco.save()
        return redirect('checkout')
    else:        
        context = {}
        return render(request, 'adicionar_endereco.html', context)

@login_required
def minha_conta(request):
    return render(request, 'usuario/minha_conta.html')

def fazer_login(request):
    erro = False
    if request.user.is_authenticated:
        return redirect('loja')
    if request.method == 'POST':
        dados=request.POST.dict()
        if 'username' in dados and 'password' in dados:
            email = dados.get('username')
            senha = dados.get('password')
            usuario = authenticate(request, username=email, password=senha)
            if usuario:
                login(request, usuario)
                return redirect('loja')
            else:
                erro = True
        else:
            erro = True
    context = { "erro:": erro}
    return render(request, 'usuario/login.html', context )

def criar_conta(request):
    
    if request.user.is_authenticated:
        return redirect('loja')
    if request.method == 'POST':
        dados=request.POST.dict()
        print('passei no post')
        if 'email' in dados and 'senha' in dados:
            email = dados.get('email')
            senha = dados.get('senha')
            cofirmacao_senha = dados.get('senha')
            print('email:', email)
            print('senha:', senha)
            print('confifracao_senha:', cofirmacao_senha)
            try:
                validate_email(email)
            except ValidationError:
                erro = "Email inválido."
                print( erro )
                context = { "erro:": erro}
                return render(request, 'usuario/criar_conta.html', context )
            if senha != cofirmacao_senha:
                erro = "As senhas não coincidem."
                print( erro )
                context = { "erro:": erro}
                return render(request, 'usuario/criar_conta.html', context )
            if User.objects.filter(username=email).exists():
                erro = "Email já cadastrado."
                print(erro)
                context = { "erro:": erro}
                return render(request, 'usuario/criar_conta.html', context )
            usuario, criado = User.objects.get_or_create(username=email, email=email)
            usuario.set_password(senha)
            usuario.save()
            print('usuario foi criado', usuario)
            ## Observe que cliente é uma tabela e usuario(django) é outra tabela, e elas estão relacionadas. O cliente tem um campo user que é uma ForeignKey para o usuário. 
            # Então, quando criamos um usuário, também precisamos criar um cliente associado a esse usuário. relacionamento 1:1
            
            if request.COOKIES.get('id_sessao'):
                ## A fim não perdemos os itens do carrinho no anônimo, vamos verificar antes de criar. 
                # Se o usuário tinha um carrinho anônimo, vamos associar esse carrinho ao novo cliente criado.
                id_sessao = request.COOKIES.get('id_sessao')
                print('tem id_sessao', id_sessao)
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                print('sem sessao')
                cliente, criado = Cliente.objects.get_or_create(email=email)
            cliente.usuario = usuario
            cliente.email=email
            cliente.save()
            print('cliente: ', cliente )
            ## fazendo o login logo após a criação da conta:
            usuario = authenticate(request, username=email, password=senha)
            if usuario:
                login(request, usuario)
                print( 'usuario foi autenticado')
                return redirect('loja')
            else:
                erro = "Erro ao autenticar o usuário após a criação da conta."
                print( 'usuario NAO fOI autenticado')
        else:
            erro = "Preencha todos os campos."
    else:
        context={"erro": erro}            
        print( request.method)
        print(context)
    return render(request, 'usuario/criar_conta.html', context )
@login_required    
def fazer_logout(request):
    print( 'usuario saiu', request.user)
    ##resposta.delete_cookie('id_sessao')
    logout(request)
    return  redirect('fazer_login')
