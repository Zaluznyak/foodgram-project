import csv
import os

from django.core.management.base import BaseCommand

from foodgram.models import Ingredients
from final_project.settings import BASE_DIR

CSV_FILE_PATH = os.path.join(BASE_DIR, "ingredients.csv")


class Command(BaseCommand):
    help = "Load ingredient"

    def handle(self, *args, **options):
        with open(CSV_FILE_PATH, encoding="utf-8") as file:
            reader = csv.reader(file)
            for name, dimen in reader:
                Ingredients.objects.get_or_create(name=name, dimension=dimen)
