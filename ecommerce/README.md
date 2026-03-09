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