def filtrar_produtos(produtos, filtro, preco_minimo=0, preco_maximo=1000, tamanho=None):
    if filtro:    
        if  "-" in filtro:
            categoria_slug, tipo_slug = filtro.split("-")
            produtos = produtos.filter(tipo__slug=tipo_slug, categoria__slug=categoria_slug,ativo=True)
        else:
            produtos = produtos.filter(categoria__slug=filtro,ativo=True)
    return produtos

def ordernar_produtos( produtos, ordem ):
    print ( "orderm: ", ordem)
    if ordem == "menor-preco":
        return produtos.order_by('preco')
    elif ordem == "maior-preco":
        return produtos.order_by('-preco')
    elif ordem == "mais-recente":
        return produtos.order_by('-id')
    elif ordem == "mais-vendido":
        lista_produtos=[]
        for produto in produtos:
            lista_produtos.append( (produto.total_vendas(), produto) )
        lista_produtos = sorted(lista_produtos, key=lambda x: x[0], reverse=True)
        produtos = [item[1] for item in lista_produtos ]
        print
        return produtos
        
    else:
        return produtos
