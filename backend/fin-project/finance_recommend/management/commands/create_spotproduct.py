from django.core.management.base import BaseCommand
from finance_recommend.models import SpotProduct, Gold, Oil, Carbon
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Gold, Oil, Carbon에 대한 SpotProduct를 생성합니다.'

    def handle(self, *args, **options):
        self.create_spot_product_from_gold()
        self.create_spot_product_from_oil()
        self.create_spot_product_from_carbon()

    def create_spot_product_from_gold(self):
        gold = Gold.objects.first()
        if gold:
            content_type = ContentType.objects.get_for_model(Gold)
            spot_product, created = SpotProduct.objects.get_or_create(
                spot_type='Gold',
                object_id=gold.id,
                defaults={
                    'name': '금 대표 상품',
                    'content_type': content_type
                }
            )
            status = 'created' if created else 'already exists'
            self.stdout.write(self.style.SUCCESS(f"Gold SpotProduct {status}: ID {spot_product.id}"))
        else:
            self.stdout.write(self.style.WARNING("Gold 데이터가 없습니다."))

    def create_spot_product_from_oil(self):
        oil = Oil.objects.first()
        if oil:
            content_type = ContentType.objects.get_for_model(Oil)
            spot_product, created = SpotProduct.objects.get_or_create(
                spot_type='Oil',
                object_id=oil.id,
                defaults={
                    'name': '유가 대표 상품',
                    'content_type': content_type
                }
            )
            status = 'created' if created else 'already exists'
            self.stdout.write(self.style.SUCCESS(f"Oil SpotProduct {status}: ID {spot_product.id}"))
        else:
            self.stdout.write(self.style.WARNING("Oil 데이터가 없습니다."))

    def create_spot_product_from_carbon(self):
        carbon = Carbon.objects.first()
        if carbon:
            content_type = ContentType.objects.get_for_model(Carbon)
            spot_product, created = SpotProduct.objects.get_or_create(
                spot_type='Carbon',
                object_id=carbon.id,
                defaults={
                    'name': '탄소배출권 대표 상품',
                    'content_type': content_type
                }
            )
            status = 'created' if created else 'already exists'
            self.stdout.write(self.style.SUCCESS(f"Carbon SpotProduct {status}: ID {spot_product.id}"))
        else:
            self.stdout.write(self.style.WARNING("Carbon 데이터가 없습니다."))
