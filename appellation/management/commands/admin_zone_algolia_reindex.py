from django.conf import settings
from django.core.management.base import BaseCommand
from algoliasearch.search_client import SearchClient
from appellation.models import AdminZone


class Command(BaseCommand):
    help = (
        "Sync AdminZone entries to algolia\n"
        "python manage.py admin_zone_algolia_reindex"
    )

    def algolia_save_objects(self, index, queryset):
        batch = []
        for e in queryset.iterator():
            batch.append(e.as_dict())
            if len(batch) == 100:
                index.save_objects(batch)
                batch = []
        index.save_objects(batch)

    def handle(self, *args, **options):
        algolia_client = SearchClient.create(
            settings.ALGOLIA["APPLICATION_ID"],
            settings.ALGOLIA["API_KEY"],
        )
        algolia_prefix = f'{settings.ALGOLIA["INDEX_PREFIX"]}_'
        # Sync Region
        index = algolia_client.init_index(f'{algolia_prefix}Region')
        queryset = AdminZone.objects.filter(hierarchy="Region")
        index.clear_objects()
        self.algolia_save_objects(index, queryset)
        self.stdout.write("Region Sync to Algolia")
        # Sync Vineyard
        index = algolia_client.init_index(f'{algolia_prefix}Vineyard')
        queryset = AdminZone.objects.filter(hierarchy="Vineyard")
        index.clear_objects()
        self.algolia_save_objects(index, queryset)
        self.stdout.write("Vineyard Sync to Algolia")
        # Sync Appellation
        index = algolia_client.init_index(f'{algolia_prefix}AdminZone')
        queryset = AdminZone.objects.filter()
        index.clear_objects()
        self.algolia_save_objects(index, queryset)
        self.stdout.write("Appellation Sync to Algolia")
