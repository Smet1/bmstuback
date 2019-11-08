from django.core.management.base import BaseCommand
from main.models import Cabinet
from django.template.loader import get_template
import os
from django.conf import settings
from itertools import chain


class Command(BaseCommand):
    help = 'Creates path between end and start points'

    def add_arguments(self, parser):
        parser.add_argument('start_id', type=int)
        parser.add_argument('end_id', type=int)

    def depth_search(self, s, end):
        # OPTIMIZE: pls
        query = Cabinet.objects.all().order_by('id')
        list_of_pks = list(map(lambda x: x, query))

        list_of_adjacency = [ set(chain(map(lambda x: list_of_pks.index(x), Cabinet.objects.filter(node=i)), [i.node_id - 1] if i.node_id else [])) for i in list_of_pks ]
        visited = [False ] * len(list_of_adjacency)
        prev = [None] * len(list_of_adjacency)

        def dfs(start):
            visited[start] = True
            for vertex in list_of_adjacency[start]:
                if not visited[vertex]:
                    prev[vertex] = start
                    dfs(vertex)

        s_pk = list_of_pks.index(s)
        dfs(s_pk)

        path = []
        current = list_of_pks.index(end)
        while current != None:
            next = prev[current]
            path.append( (list_of_pks[current], list_of_pks[next if next else s_pk]) )
            current = next

        return path


    def handle(self, start_id, end_id, **options):
        print('finding path')
        start = Cabinet.objects.get(pk=start_id)
        end = Cabinet.objects.get(pk=end_id)

        # OPTIMIZE: preload only need
        graph = Cabinet.objects.all()

        path = self.depth_search(start, end)

        plan = get_template('bmstuplan_to_render.svg')
        with open(os.path.join(settings.BASE_DIR, 'paths/bmstuplan_{}_to_{}.svg').format(start.pk, end.pk), 'w', encoding="utf-8") as file:
            file.write(plan.render({'path': path, 'start': start, 'end': end}))
