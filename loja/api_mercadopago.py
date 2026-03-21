## Instale antes: 
## pip3 install python-dotenv mercadopago

import mercadopago
from mercadopago.resources import preference
from dotenv import load_dotenv
import os

load_dotenv()

public_key = os.getenv("MP_PUBLIC_KEY")
token = os.getenv("MP_ACCESS_TOKEN")

def criar_pagamento( itens_pedido, link):

    sdk = mercadopago.SDK(token)
    itens=[]

    for item in itens_pedido:
        #print ("Item do pedido:", item)
        quantidade = int(item.quantidade)
        preco_unitario = float( item.item_estoque.produto.preco)
        nome_produto = item.item_estoque.produto.nome
        itens.append({
            "title": nome_produto,
            "quantity": quantidade,
            "unit_price": preco_unitario
        })

    preference_data = {
        "items": itens,
        "back_urls": {
                "success": link,
                "failure": link,
                "pending": link
        },
        
    }
    preference_response = sdk.preference().create(preference_data)
    preference= preference_response["response"]
    link_pagamento = preference["init_point"]
    

    ##id_pagamento=link_pagamento["response"]["id"]


    print(preference_response["status"])        # ex: 201
    ##print(preference_response["response"])      # dict com os dados

    id_pagamento = preference_response["response"]["id"]
    link_pagamento = preference_response["response"]["init_point"]  # link de pagamento
    print("Link para pagamento:", link_pagamento)
    print ("id pagamento:", id_pagamento)
    return link_pagamento, id_pagamento
