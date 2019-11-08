from django.core.management.base import BaseCommand
from main.models import Cabinet
from django.template.loader import get_template
import os
from django.conf import settings
from itertools import chain


class Command(BaseCommand):
    help = 'Creates path between end and start points'

    def add_arguments(self, parser):
        parser.add_argument('node_id', type=int)

    def handle(self, node_id, *args, **options):
        cabinet = Cabinet.objects.get(id=node_id)
        templ = get_template('bmstuplan_node.svg')

        context = {
            'node': cabinet
        }

        with open(os.path.join(settings.BASE_DIR, 'paths/bmstunode_{}.svg').format(cabinet.pk), 'w', encoding="utf-8") as file:
            file.write(templ.render(context))
