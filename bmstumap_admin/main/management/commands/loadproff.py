from django.core.management.base import BaseCommand
from main.models import Employee
from django.template.loader import get_template
import os
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('proff.txt', 'r', encoding="utf-8") as file:
            data = file.read().split('\n')

        for i in filter(lambda x: x, data):
            # print(i)
            last, first, middle = i.split(' ')
            Employee.objects.create(
                last_name=last,
                first_name=first,
                middle_name=middle
            )
