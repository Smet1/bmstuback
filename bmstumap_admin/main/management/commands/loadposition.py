from django.core.management.base import BaseCommand
from main.models import Position
from django.template.loader import get_template
import os
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('position.txt', 'r', encoding="utf-8") as file:
            data = file.read().split('\n')

        for i in filter(lambda x: x, data):
            # print(i)
            Position.objects.create(
                name=i
            )
