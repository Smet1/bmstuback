from django.core.management.base import BaseCommand
from main.models import Cabinet
from django.template.loader import get_template
from django.conf import settings
import os


class Command(BaseCommand):

    def handle(*args, **kwargs):
        plan = get_template('bmstuplan_all.svg')
        file_to_save = 'paths/bmstuplan_all.svg'
        context = {
            'markers': Cabinet.objects.filter(auditoria=True)
        }

        with open(os.path.join(settings.BASE_DIR, file_to_save), 'w', encoding="utf-8") as file:
            file.write(plan.render(context))
