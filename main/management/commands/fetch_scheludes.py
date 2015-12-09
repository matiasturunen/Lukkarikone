from django.core.management.base import BaseCommand, CommandError
from main.parser import parser
from main.models import Schelude

class Command(BaseCommand):
    help = 'Fetches scheludes from internet and deletes existing ones'
    
    def handle(self, *args, **options):
        print("Hangling...")
        # flush all tables related to schelude
        Schelude.objects.all().delete()
        # get new scheludes
        ok = parser.fetchScheludes()
        self.stdout.write('Hangling done. Success: {0}'.format(ok))