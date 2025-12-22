from django.core.management import BaseCommand
from tools import gen_api_client


class Command(BaseCommand):
    help = "API Client Codegen"

    def handle(self, *args, **options):
        gen_api_client.main()
