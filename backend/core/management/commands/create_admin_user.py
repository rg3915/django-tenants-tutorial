from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

'''
Usage: python manage.py create_admin_user -p sua-senha
'''


class Command(BaseCommand):
    help = "Cria um super usuário admin."

    def add_arguments(self, parser):
        parser.add_argument('-p', dest='password', help='Digite a senha.')

    def handle(self, *args, **options):
        password = options.get('password')

        if not password:
            print('Digite -p e informe a senha.')
            return

        if User.objects.filter(username='lorem').exists():
            print('admin já existe!')
        else:
            User.objects.create_superuser('lorem', 'admin@email.com', password)
