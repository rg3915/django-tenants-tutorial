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

Opcionalmente você pode rodar o [Portainer](https://docs.portainer.io/start/install/server/docker)

```
docker run -d \
--name myportainer \
-v /opt/portainer:/data \
portainer/portainer
```



# links

https://django-tenants.readthedocs.io/en/latest/index.html

https://github.com/django-tenants/django-tenants

https://youtu.be/TWF7okf5Xoo

https://youtu.be/IrAz-q5rv3A

https://blog.4linux.com.br/schemas-e-namespaces-postgresql-com-django/


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

## Configura o banco de dados em settings.py

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': config('POSTGRES_DB', 'db'),  # postgres
        'USER': config('POSTGRES_USER', 'postgres'),
        'PASSWORD': config('POSTGRES_PASSWORD', 'postgres'),
        # 'db' caso exista um serviço com esse nome.
        'HOST': config('DB_HOST', '127.0.0.1'),
        'PORT': 5433,
    }
}
```


## Criando schemas manualmente

![](img/schema.png)

E acompanhar pelo pgAdmin.

```
docker container exec -it db psql


CREATE DATABASE test;
\l
\c test

CREATE SCHEMA my_schema01;
\dn

CREATE TABLE my_schema01.cities (id SERIAL PRIMARY KEY, city VARCHAR(50), uf VARCHAR(2));
\dt my_schema01.*

INSERT INTO my_schema01.cities (city, uf) VALUES ('São Paulo', 'SP');
SELECT * FROM my_schema01.cities;

CREATE SCHEMA my_schema02;
\dn

CREATE TABLE my_schema02.cities (id SERIAL PRIMARY KEY, city VARCHAR(50), uf VARCHAR(2));
\dt my_schema02.*

INSERT INTO my_schema02.cities (city, uf) VALUES ('Bahia', 'BA');
SELECT * FROM my_schema02.cities;

DROP TABLE my_schema01.cities;
DROP TABLE my_schema02.cities;

DROP SCHEMA my_schema01;
DROP SCHEMA my_schema02;
\dn

docker container stop pgadmin

\c postgres
DROP DATABASE test;
\l
```

## Configurando Tenant

### Cria app tenant

```
cd backend
python ../manage.py startapp tenant
cd ..
```

### Edita apps.py

```python
# tenant/apps.py
...
name = 'backend.tenant'
```

### Edita models.py

```python
# tenant/models.py
from django.db import models
from django_tenants.models import DomainMixin, TenantMixin


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True


class Domain(DomainMixin):
    ...
```

### Edita admin.py

```python
# tenant/admin.py
from django.apps import apps
from django.contrib import admin
from django_tenants.utils import get_public_schema_name


class TenantsAdmin(admin.ModelAdmin):
    '''
    Hides public models from tenants
    https://stackoverflow.com/a/66898816
    '''

    def has_view_permission(self, request, view=None):
        try:
            if request.tenant.schema_name == get_public_schema_name():
                return True
            return False
        except AttributeError:
            return True
        except Exception as e:
            raise e

    def has_add_permission(self, request, view=None):
        return False

    def has_change_permission(self, request, view=None):
        return False

    def has_delete_permission(self, request, view=None):
        return False

    def has_view_or_change_permission(self, request, view=None):
        try:
            if request.tenant.schema_name == get_public_schema_name():
                return True
            return False
        except AttributeError:
            return True
        except Exception as e:
            raise e


app = apps.get_app_config('tenant')
for model_name, model in app.models.items():
    admin.site.register(model, TenantsAdmin)
```

Deletando algumas coisas

```
rm -f backend/tenant/tests.py
rm -f backend/tenant/views.py
```

### settings.py

```python
# settings.py
SHARED_APPS = (
    'django_tenants',  # mandatory
    'backend.tenant',  # you must list the app where your tenant model resides in
    # 'backend.company',

    # everything below here is optional
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # others apps
    'django_extensions',
)

TENANT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # your tenant-specific apps
    # 'backend.core',
    # 'backend.crm',
    # 'backend.sale',
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

TENANT_MODEL = "tenant.Client"  # app.Model

TENANT_DOMAIN_MODEL = "tenant.Domain"  # app.Model


MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',  # <<<
    'django.middleware.security.SecurityMiddleware',
    ...
]

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)
```

```
python manage.py makemigrations            # caso tenha alterações nos models
python manage.py migrate_schemas --shared
python manage.py create_tenant             # Cria um novo tenant
python manage.py create_tenant_superuser   # Cria um novo super user para o tenant escolhido
python manage.py migrate_schemas
```

```
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

Já podemos acessar

```
acme.localhost:8000/admin
stark.localhost:8000/admin
```

Crie esses dois usuários.

stark: Howard Stark, Tony Stark



Se você acessar localhost:8000/admin vai dar erro, então


### Configurando settings.py

```
cp backend/urls.py backend/urls_public.py
```


```python
# settings.py
PUBLIC_SCHEMA_URLCONF = 'backend.urls_public'

SHOW_PUBLIC_IF_NO_TENANT_FOUND = True
```


## Acessando o shell_plus para cada tenant

```
python manage.py tenant_command shell_plus --schema=stark
```

```python
>>> User.objects.all()
<QuerySet [<User: admin>, <User: howard>, <User: tony>]>
```

```
python manage.py tenant_command shell_plus --schema=acme
```

Crie o usuário

acme: stewart


```python
>>> User.objects.all()
<QuerySet [<User: admin>, <User: stewart>]>
```


## App company com model Company OneToOne(Client)

Company deve ser global.

```
cd backend
python ../manage.py startapp company
cd ..
```

### Edita apps.py

```python
# company/apps.py
...
name = 'backend.company'
```


### Edita models.py

```python
# company/models.py
from django.db import models

from backend.tenant.models import Client


class Company(models.Model):
    name = models.CharField('nome', max_length=100, unique=True)
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        verbose_name='cliente',
        related_name='companies',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'

    def __str__(self):
        return f'{self.name}'
```

### Edita tenant/admin.py

```python
# tenant/admin.py

...

class CompanyAdmin(admin.ModelAdmin):
    '''
    Hides public models from tenants
    https://stackoverflow.com/a/66898816
    '''
    readonly_fields = ('client',)

    def has_view_permission(self, request, view=None):
        try:
            if request.tenant.schema_name == get_public_schema_name():
                return True
            return False
        except AttributeError:
            return True
        except Exception as e:
            raise e

    def has_add_permission(self, request, view=None):
        return False

    def has_change_permission(self, request, view=None):
        try:
            if request.tenant.schema_name == get_public_schema_name():
                return True
            return False
        except AttributeError:
            return True
        except Exception as e:
            raise e

    def has_delete_permission(self, request, view=None):
        return False

    def has_view_or_change_permission(self, request, view=None):
        try:
            if request.tenant.schema_name == get_public_schema_name():
                return True
            return False
        except AttributeError:
            return True
        except Exception as e:
            raise e


...


app = apps.get_app_config('company')
for model_name, model in app.models.items():
    admin.site.register(model, CompanyAdmin)
```

Deletando algumas coisas

```
rm -f backend/company/admin.py
rm -f backend/company/tests.py
rm -f backend/company/views.py
```

### Edita settings.py

```python
SHARED_APPS = (
    'django_tenants',  # mandatory
    'backend.tenant',  # you must list the app where your tenant model resides in
    'backend.company',
    ...
)
```

### Migrações

```
python manage.py makemigrations
python manage.py migrate
```

> Repare que temos Empresa no Admin público, mas não no tenant.



## App crm com model Employee OneToOne(User)




## Ao cadastrar o funcionário, cria o usuário e o associa ao funcionário.




## App sale com model Sale, com employee(FK)




## Configurando Admin




## App core com o template principal




    lista: clientes, funcionários e vendas
## App crm com lista de clientes e funcionários




## App sale com a lista de vendas





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

