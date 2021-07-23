from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pathlib import Path
import json

class Command(BaseCommand):
    """Create a default superuser if not existed"""
    def handle(self, *args, **options):
        self.stdout.write('Creating superuser...')
        name, email, password = self.get_superuser_info()
        user_exists = self.check_user_exists(email)
        if not user_exists:
            User.objects.create_superuser(name, email, password)
            self.stdout.write('Default superuser created')
        else:
            self.stdout.write('Default superuser already exists')

    def get_superuser_info(self):
        with open(Path(__file__).parent.parent.parent.parent / 'ContactManager/cred.txt', 'r') as f:
            ENV_CONFIG = json.loads(f.read())
        return (ENV_CONFIG['SUPERUSER_NAME'],
                ENV_CONFIG['SUPERUSER_EMAIL'],
                ENV_CONFIG['SUPERUSER_PASS'])

    def check_user_exists(self, email):
        user = User.objects.filter(email=email)
        return True if user else False
