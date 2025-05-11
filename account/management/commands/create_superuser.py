from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser if it doesn\'t exist'

    def add_arguments(self, parser):
        parser.add_argument('--noinput', action='store_true', help='Run the command without any prompts')

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            if not options['noinput']:
                self.stdout.write('Superuser already exists')
            return

        username = settings.DJANGO_SUPERUSER_USERNAME
        email = settings.DJANGO_SUPERUSER_EMAIL
        password = settings.DJANGO_SUPERUSER_PASSWORD

        if not all([username, email, password]):
            self.stderr.write('Superuser creation skipped. Please set DJANGO_SUPERUSER_USERNAME, '
                           'DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD in your environment.')
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {username}'))
