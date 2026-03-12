def filtrar_produtos(produtos, filtro):
    from .models import Produto, Categoria
    if filtro:    
        if  "-" in filtro:
            categoria_slug, tipo_slug = filtro.split("-")
            produtos = produtos.filter(tipo__slug=tipo_slug, categoria__slug=categoria_slug,ativo=True)
            produtos = Produto.objects.filter(tipo__slug=tipo_slug,ativo=True)
        else:
            produtos = produtos.filter(categoria__nome=filtro,ativo=True)
    return produtos