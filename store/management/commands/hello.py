from django.core.management.base import BaseCommand
#from django.contrib.auth.models import User
#from ...models import Product

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Hello")