from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Create groups if not available"""
    def handle(self, *args, **options):
        self.stdout.write('Creating groups...')
        gp_created = False
        if not Group.objects.filter(name='customer'):
            Group.objects.create(name='customer')
            gp_created = True
        if not Group.objects.filter(name='admin'):
            Group.objects.create(name='admin')
            gp_created = True

        self.stdout.write(self.style.SUCCESS('Groups created!' if gp_created else 'Groups already exist!'))
