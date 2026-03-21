### Requisitos

 python3 -m venv .venv

source .venv/bin/activate  
pip install django   
python -m pip install Pillow

### crie o admin

python3 manage.py createsuperuser

Dia a dia

source .venv/bin/activate

cursor .   
python3 manage.py runserver

### ALTERANDO TABELAS

depois de alterar o models.py execute os comandos abaixo:

python3 manage.py  makemigrations   
python3 manage.py  migrate   

python3 manage.py  runserver 

### CONFIGURE O GIT

git init .

### CRIANDO A TABELA BANNER

PASSO 01: criar tabela no models: class Banner(models.Model)

```plaintext
class Banner(models.Model):
    ativo = models.BooleanField(default=True)
    imagem =  models.ImageField(null=True, blank=True) # "banner.png"
    link_destino= models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
      return f"Link: {self.link_destino}, Ativo: {self.ativo}"
```

         
PASSO 02:Atualizar o modelo de banco de dados

```plaintext
python3 manage.py makemigrations
python3 manage.py migrate
```

PASSO 03: Fazer aparecer no admin do django  
   Registrar no admin.py para aparecer no admin django

```plaintext
admin.site.register(Banner)
```

PASSO 04:No views.py crie o banners e passe como contexto

```plaintext
def homepage(request):
   banners = Banner.objects.filter(ativo=True)
   context = {
       'banners': banners
   }
   return render(request, 'homepage.html', context)
```

PASSO 05: Agora no html ele já fica visivel:

```plaintext
{% for banner in banners %}
   <div class="banner">
       <img src="{{ banner.imagem.url }}" alt="{{ banner.titulo }}" width="800" height="300">
       <h4>{{ banner.titulo }}</h4>
   </div>
{% endfor %}
```

TABELAS DE CORES: 

[https://www.homehost.com.br/blog/tutoriais/tabela-de-cores-html/](https://www.homehost.com.br/blog/tutoriais/tabela-de-cores-html/)

QUERYSETS DJANGO: vale à pena da uma olhada. 

[https://docs.djangoproject.com/en/6.0/ref/models/querysets/](https://docs.djangoproject.com/en/6.0/ref/models/querysets/)

[https://docs.djangoproject.com/en/6.0/howto/deployment/](https://docs.djangoproject.com/en/6.0/howto/deployment/)

Veja o exemplo de quantidade > 0. Usasse \_\_gt e tem muitos outros: itens\_estoque = ItemEstoque.objects.filter(\_produto\_=produto, \_quantidade\_\_gt\_=0)

### FONT-AWESOME

[https://cdnjs.com/libraries/font-awesome](https://cdnjs.com/libraries/font-awesome)

Adicione o link abaixo no seu base.html

\<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css" integrity="sha512-2SwdPD6INVrV/lHTZbO2nodKhrnDdJK9/kg2XD1r9uGqPo1cUbujc+IYdlYdEErWNu69gVcYgdxlmVmzTWnetw==" crossorigin="anonymous" referrerpolicy="no-referrer">

### DJANDO E SESSÕES DE NAVEGADOR ( cookies ) 

### Como funciona o fluxo básico - SESSÃO

1.  **Usuário acessa o site** → Django cria uma sessão no servidor e gera um **Session ID** único
2.  **Django envia um cookie** chamado `sessionid` para o navegador
3.  **Nas próximas requisições**, o navegador envia esse cookie automaticamente
4.  **Django usa o Session ID** para buscar os dados da sessão armazenados no servido

Django cuida de tudo via `request.session` como um dicionário Python simples

```plaintext
resposta.set_cookie(key='id_sessao',value=id_sessao, max_age=30*24*60*60) # Cookie válido por 30 dias
```

_outra opção é colocar a opção **expires**_

```plaintext
from datetime import datetime request.session.set_expiry(datetime(2026, 12, 31, 23, 59))
```

### Fluxo de navegação (como está hoje)

O fluxo abaixo descreve as páginas/rotas principais e **quem chama quem** (templates → views → redirects).

#### Rotas principais

`**/**` → `homepage(request)` → renderiza `homepage.html`

*   Mostra banners ativos (`Banner.objects.filter(ativo=True)`).

`**/loja/**` → `loja(request, slug_categoria=None)` → renderiza `loja.html`

*   Lista produtos ativos.

`**/loja/<slug_categoria>/**` → `loja(request, slug_categoria)` → renderiza `loja.html`

*   Usado quando o usuário clica em uma categoria/tipo no menu.
*   Observação: `slug_categoria` pode vir no formato `categoria-tipo` (ex.: `feminino-calca`), que é interpretado no filtro de produtos.

`**/produto/<id_produto>/**` → `ver_produto(request, id_produto)` → renderiza `ver_produto.html`

*   Mostra produto, cores e tamanhos disponíveis em estoque.

`**/produto/<id_produto>/<id_cor>/**` → `ver_produto(request, id_produto, id_cor)` → renderiza `ver_produto.html`

*   Seleciona uma cor e passa `cor_selecionada` ao template.

#### Fluxo “Adicionar ao carrinho”

`**ver_produto.html**` envia POST para `**/adicionar_carrinho/<id_produto>/**`

*   Campos enviados: `tamanho` (radio) e `id_cor` (hidden).

`**/adicionar_carrinho/<id_produto>/**` → `adicionar_carrinho(request, id_produto)`

*   Procura o `ItemEstoque` pela combinação `(produto, cor, tamanho)`.
*   Cria/recupera `Pedido` aberto (`finalizado=False`) do cliente.
*   Cria/recupera `ItensPedido` e incrementa `quantidade`.
*   Dá `redirect('carrinho')` ao final (padrão POST/Redirect/GET).
*   Se usuário não estiver logado, usa cookie `id_sessao` para associar um `Cliente` (sessão).

#### Fluxo “Carrinho”

*   `**/carrinho/**` → `carrinho(request)` → renderiza `carrinho.html`
    *   Recupera/cria o `Pedido` aberto do cliente e lista `ItensPedido`.
    *   Se não existir `id_sessao` no cookie (usuário anônimo “novo”), renderiza o carrinho com `cliente_existente=False`.

#### Fluxo “Remover do carrinho”

*   **Template do carrinho** envia POST para `**/remover_carrinho/<id_produto>/**`
*   `**/remover_carrinho/<id_produto>/**` → `remover_carrinho(request, id_produto)`
    *   Decrementa `ItensPedido.quantidade`, devolve 1 unidade ao estoque e apaga item se `quantidade &lt;= 0`.
    *   Depois faz `redirect('carrinho')`.

#### Fluxo “Checkout” e “Endereços”

`**/checkout/**` → `checkout(request)` → renderiza `checkout.html`

*   Recupera `Pedido` aberto e lista `Endereco` do cliente.

`**/adicionar_endereco**` → `adicionar_endereco(request)`

*   **GET**: renderiza `adicionar_endereco.html`
*   **POST**: cria `Endereco` e faz `redirect('checkout')`

#### Links globais (navbar)

*   O `navbar.html` aparece nas páginas (via `base.html`).
*   Ele chama as rotas por nome:
    *   `homepage`, `loja`, `login`, `minha_conta`, `carrinho`
*   Ele também monta links de categoria/tipo para a rota `loja` com o slug:
    *   Categoria: `loja/<categoria.slug>/`
    *   Tipo: `loja/<categoria.slug>-<tipo.slug>/`\</tipo.slug>\</categoria.slug>\</categoria.slug>

### _@login\_required e LOGIN\_URL = 'fazer\_login'_

_Para forçar a autorização temos no django : from django.contrib.auth.decorators import login\_required_

_A variável LOGIN\_URL é definida no settings.py_

_Em cada função na view, coloque o decorators @login\_required_

_exemplo:_

```plaintext
@login_required
def fazer_logout(request):
    logout(request)
    return redirect('fazer_login')
```

### URLS PRONTAS DO DJANGO PARA CONTAS

Usando urls do django para controle da conta do usuário:

Altere o arquivo urls.py

```plaintext
from django.contrib.auth import views
path('password_change/', views.PasswordChangeView.as_view, _name_="password_change"),
path('password_change/done/', views.PasswordChangeDoneView.as_view, _name_="password_change_done"),
path('password_reset/', views.PasswordResetView.as_view, _name_="password_reset"),
path('password_reset/done/', views.PasswordResetDoneView.as_view, _name_="password_reset_done"),
path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view, _name_="password_reset_confirm"),
path('reset/done/', views.PasswordResetCompleteView.as_view, _name_="password_reset_complete"),
```

exemplo de uso: veja o arquivo login.html que temos uma chamada:

\<a href="{% url 'password\_reset' %}" title="{% url 'password\_reset' %}">Esqueci minha senha\</a>

### SMTP EMAIL

```plaintext
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'sua-senha-de-app'  # senha de app, não a senha normal
DEFAULT_FROM_EMAIL = 'seu-email@gmail.com'
```

O ideal é usar variável de ambiente. 

\`\`\`plaintext

## settings.py

import os  
EMAIL\_HOST\_USER = os.environ.get('EMAIL\_HOST\_USER')  
EMAIL\_HOST\_PASSWORD = os.environ.get('EMAIL\_HOST\_PASSWORD')  
\`\`\`

### MERCADO PAGO

[https://www.mercadopago.com.br/developers/pt](https://www.mercadopago.com.br/developers/pt)

[https://www.mercadopago.com.br/developers/pt/docs/sdks-library/server-side](https://www.mercadopago.com.br/developers/pt/docs/sdks-library/server-side)

[https://github.com/mercadopago/sdk-python](https://github.com/mercadopago/sdk-python)

criar preferência:

[https://www.mercadopago.com.br/developers/pt/reference/online-payments/checkout-pro/preferences/create-preference/post](https://www.mercadopago.com.br/developers/pt/reference/online-payments/checkout-pro/preferences/create-preference/post)

```plaintext
pip3 install mercadopago
```

No caso você tem que pegar o token do MERCADO PAGO:

```plaintext
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
print (preference_response)
```

_\## Para testar no comando de linha, abra um terminal e na pasta onde está este arquivo execute assim:_

_python3 api\_mercadopago.py_

_\## Lembre-se de abrir como anônimo para dar certo._

_\## o legal deste print, é que se copiarmos a url de init\_point, e colarmos no navegador como anônimo, ele vai abrir a tela de pagamento do MercadoPago, onde podemos testar o processo de pagamento._

_\## como queremos pegar o link para o pagamento, então vamos fazer assim:_

link\_pagamento = preference\["init\_point"\]

print("Link para pagamento:", link\_pagamento)

\_## saída: Link para pagamento: https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=3281994042-50624590-76e1-4b40-a2d2-978dbab63534\_

_\## pegando o id\_pagamento:_

_\## aqui estamos pegando o id do pagamento, que é o pref\_id que está presente na url de init\_point._

id\_pagamento=link\_pagamento\["response"\]\["id"\]

print ("id pagamento:", id\_pagamento)

SMTP COM GMAIL

Configure o settings.py

```plaintext
import os
from dotenv import load_dotenv

load_dotenv()

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = os.getenv('EMAIL_PORT')
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

no arquivo .env coloque seus dados. Veja o env-example.

EMAIL\_HOST=smtp.gmail.com EMAIL\_PORT=587 EMAIL\_USE\_TLS=True EMAIL\_HOST\_USER=seu@email.com EMAIL\_HOST\_PASSWORD=sua\_senha