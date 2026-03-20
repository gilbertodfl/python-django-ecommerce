## Instale antes: 
## pip3 install python-dotenv mercadopago

import mercadopago
from mercadopago.resources import preference
from dotenv import load_dotenv
import os

load_dotenv()

public_key = os.getenv("MP_PUBLIC_KEY")
token = os.getenv("MP_ACCESS_TOKEN")

sdk = mercadopago.SDK(token)
preference_data = {
    "items": [
        {
            "title": "Produto Exemplo",
            "quantity": 1,
            "unit_price": 10.00
        },
        "back_urls": {
            "success": "https://www.sualoja.com/success",
            "failure": "https://www.sualoja.com/failure",
            "pending": "https://www.sualoja.com/pending"
        },
    ]
}
preference_response = sdk.preference().create(preference_data)
preference= preference_response["response"]
## Para testar no comando de linha, abra um terminal e na pasta onde está este arquivo execute assim:
## python3 api_mercadopago.py
##print (preference_response)

## Lembre-se de abrir como anônimo para dar certo. 
## o legal deste print, é que se copiarmos a url de init_point, e colarmos no navegador como anônimo, ele vai abrir a tela de pagamento do MercadoPago, onde podemos testar o processo de pagamento.

## como queremos pegar o link para o pagamento, então vamos fazer assim:
link_pagamento = preference["init_point"]
print("Link para pagamento:", link_pagamento)

## saída: Link para pagamento: https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=3281994042-50624590-76e1-4b40-a2d2-978dbab63534

## pegando o id_pagamento: 
## aqui estamos pegando o id do pagamento, que é o pref_id que está presente na url de init_point.
id_pagamento=link_pagamento["response"]["id"]
print ("id pagamento:", id_pagamento)
