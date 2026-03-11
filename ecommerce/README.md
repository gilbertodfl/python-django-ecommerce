 python3 -m venv .venv

 source .venv/bin/activate  
pip install django   
python -m pip install Pillow

python3 manage.py  makemigrations   
python3 manage.py  migrate   
python3 manage.py createsuperuser

python3 manage.py  runserver 

git init .

EXTENSÕES INTERESSANTES DE INSTALAR

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
   admin.site.register(Banner)  
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

Veja o exemplo de quantidade > 0. Usasse \_\_gt e tem muitos outros: itens\_estoque = ItemEstoque.objects.filter(\_produto\_=produto, \_quantidade\_\_gt\_=0)

### FONT-AWESOME

[https://cdnjs.com/libraries/font-awesome](https://cdnjs.com/libraries/font-awesome)

Adicione o link abaixo no seu base.html

\<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css" integrity="sha512-2SwdPD6INVrV/lHTZbO2nodKhrnDdJK9/kg2XD1r9uGqPo1cUbujc+IYdlYdEErWNu69gVcYgdxlmVmzTWnetw==" crossorigin="anonymous" referrerpolicy="no-referrer">

### DJANDO E SESSÕES DE NAVEGADOR ( cookies ) 

### Como funciona o fluxo básico

1.  **Usuário acessa o site** → Django cria uma sessão no servidor e gera um **Session ID** único
2.  **Django envia um cookie** chamado `sessionid` para o navegador
3.  **Nas próximas requisições**, o navegador envia esse cookie automaticamente
4.  **Django usa o Session ID** para buscar os dados da sessão armazenados no servido

Django cuida de tudo via `request.session` como um dicionário Python simples

```plaintext
resposta.set_cookie(key='id_sessao',value=id_sessao, max_age=30*24*60*60) # Cookie válido por 30 dias
```

_outra opção é colocar a opção expires_

```plaintext
from datetime import datetime request.session.set_expiry(datetime(2026, 12, 31, 23, 59))
```