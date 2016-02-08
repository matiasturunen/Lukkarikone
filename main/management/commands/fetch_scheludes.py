from django.core.management.base import BaseCommand, CommandError
from main.parser import parser
from main.models import Schelude
from main.errors import FetchError
from django.db import transaction

class Command(BaseCommand):
    help = 'Fetches scheludes from internet and deletes existing ones'
    
    @transaction.atomic
    def handle(self, *args, **options):
        print("Handling...")
        # flush all tables related to schelude
        Schelude.objects.all().delete()
        
        # get new scheludes
        ok = parser.fetchScheludes()
        if (not ok):
            # Not able to get all required scheludes.
            # Raise exception and transaction will be rolled back
            raise FetchError("Scheludes couldn't be fetched, rolling back!")

        self.stdout.write('Handling done. Success: {0}'.format(ok))