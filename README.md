# django-tenants-tutorial

Tutorial baseado em https://django-tenants.readthedocs.io/en/latest/index.html


## Este projeto foi feito com:

* [Python 3.10.4](https://www.python.org/)
* [Django 4.0.7](https://www.djangoproject.com/)
* [django-tenants 3.4.3](https://django-tenants.readthedocs.io/en/latest/)
* [Bulma CSS](https://bulma.io/)

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/rg3915/django-tenants-tutorial.git
cd django-tenants-tutorial
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py

docker-compose up -d  # O objetivo é rodar o PostgreSQL

python manage.py migrate
python manage.py createsuperuser --username="admin" --email=""
```

# links

https://django-tenants.readthedocs.io/en/latest/index.html

https://github.com/django-tenants/django-tenants

https://youtu.be/TWF7okf5Xoo

https://youtu.be/IrAz-q5rv3A


# Passo a passo para criar do zero

```
git checkout base
```

# Parte 1

## Instalação

```
pip install -U pip
pip install Django==4.0.7 django-tenants==3.4.3 django-extensions psycopg2-binary python-decouple
```

## Cria o projeto

**Obs:** Na verdade já foi criado na branch.

```
django-admin startproject backend .
```

Configura o settings.py com o básico (já está pronto!).

```python
# settings.py
from pathlib import Path
from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())

# ...

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR.joinpath('staticfiles')
```

### Gera as variáveis de ambiente

Daqui pra baixo precisar implementar...

```
python contrib/env_gen.py
```



## Configurando settings.py

```python
# settings.py
PUBLIC_SCHEMA_URLCONF = 'backend.urls_public'
SHOW_PUBLIC_IF_NO_TENANT_FOUND = True
```



## Como rodar o projeto

```
docker-compose up -d  # opcional, usando PostgreSQL no Docker

python manage.py makemigrations            # caso tenha alterações nos models
python manage.py migrate_schemas --shared
python manage.py create_tenant             # Cria um novo tenant
python manage.py create_tenant_superuser   # Cria um novo super user para o tenant escolhido
python manage.py migrate_schemas

schema name: acme
name: Acme Corp.
on trial: True
domain: acme.localhost
is_primary: True

schema name: stark
name: Stark Industries
on trial: True
domain: stark.localhost
is_primary: True
```

Crie esses dois usuários.

stark: Howard Stark, Tony Stark



## Acessando o shell_plus para cada tenant

```
python manage.py tenant_command shell_plus --schema=stark
```

```python
>>> Employee.objects.all()
<QuerySet [<Employee: Howard Stark>, <Employee: Tony Stark>]>
```


* App company com model Company OneToOne(Client)
* Company deve ser global
* App crm com model Employee OneToOne(User)
* Ao cadastrar o funcionário, cria o usuário e o associa ao funcionário.
* App sale com model Sale, com employee(FK)
* Configurando Admin
* App core com o template principal
    lista: clientes, funcionários e vendas
* App crm com lista de clientes e funcionários
* App sale com a lista de vendas

```
cp backend.urls.py backend.urls_public.py
```

No template `{{ request.tentant.name }}`

### App core com o template principal
    lista: clientes, funcionários e vendas

```
mkdir backend/core/templates
touch backend/core/templates/index.html
```



### App crm com lista de clientes e funcionários

```
touch backend/crm/urls.py

mkdir -p backend/crm/templates/crm
touch backend/crm/templates/crm/customer_list.html
touch backend/crm/templates/crm/employee_list.html
```



### App sale com a lista de vendas

```
touch backend/sale/urls.py

mkdir -p backend/sale/templates/sale
touch backend/sale/templates/sale/sale_list.html
```

