from .models import Pedido, ItensPedido, Cliente
def carrinho(request):
    quantidade_produtos_carrinho = 0
    if request.user.is_authenticated:
        # Aqui você pode implementar a lógica para obter a quantidade real de produtos no carrinho do usuário
        #print ('Usuário autenticado:', request.user.username)
        cliente = request.user.cliente
    else:
        if request.COOKIES.get('id_sessao'):
            id_sessao = request.COOKIES.get('id_sessao')
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)    
        else:
            return { 'quantidade_produtos_carrinho': quantidade_produtos_carrinho }
       
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    ##uma vez obtido o pedido, vamos ver quantos itens fazem parte do pedido para nossos calculos de quantidade_produtos_carrinho
    ##itens_pedido = pedido.itens_pedido.all()
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)
    quantidade_produtos_carrinho = sum(item.quantidade for item in itens_pedido)
    return {'quantidade_produtos_carrinho': quantidade_produtos_carrinho}

"""
Explicando a linha: pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
pedido (à esquerda) é o campo ForeignKey do modelo ItensPedido.
pedido (à direita) é o objeto Pedido que você obteve com o get_or_create.
O Django ORM faz automaticamente:
    Internamente o campo pedido guarda só o pedido_id.
    Quando você faz filter(pedido=pedido), ele converte isso para
    WHERE pedido_id = pedido.pk.
Ou seja: você passa o objeto inteiro, e o Django “se vira” para comparar usando a chave primária (id) desse objeto.

Veja o mesmo acontece com itens_pedido = ItensPedido.objects.filter(pedido=pedido)
Onde pedido é a foreignkey do modelo ItensPedido, e o pedido é o objeto Pedido que você obteve com o get_or_create. 
O Django ORM converte isso para WHERE pedido_id = pedido.pk.
"""