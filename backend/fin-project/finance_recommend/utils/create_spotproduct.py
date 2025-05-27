from django.contrib.contenttypes.models import ContentType
from finance_recommend.models import SpotProduct, Gold, Oil, Carbon

def create_spot_product_from_gold():
    gold_instance = Gold.objects.first()
    if gold_instance:
        content_type = ContentType.objects.get_for_model(Gold)
        spot_product, created = SpotProduct.objects.get_or_create(
            spot_type='Gold',
            object_id=gold_instance.id,
            defaults={
                'name': '금 대표 상품',
                'content_type': content_type
            }
        )
        print(f"Gold SpotProduct {'created' if created else 'already exists'}: ID {spot_product.id}")
    else:
        print("Gold 데이터가 없습니다.")

def create_spot_product_from_oil():
    oil_instance = Oil.objects.first()
    if oil_instance:
        content_type = ContentType.objects.get_for_model(Oil)
        spot_product, created = SpotProduct.objects.get_or_create(
            spot_type='Oil',
            object_id=oil_instance.id,
            defaults={
                'name': '유가 대표 상품',
                'content_type': content_type
            }
        )
        print(f"Oil SpotProduct {'created' if created else 'already exists'}: ID {spot_product.id}")
    else:
        print("Oil 데이터가 없습니다.")

def create_spot_product_from_carbon():
    carbon_instance = Carbon.objects.first()
    if carbon_instance:
        content_type = ContentType.objects.get_for_model(Carbon)
        spot_product, created = SpotProduct.objects.get_or_create(
            spot_type='Carbon',
            object_id=carbon_instance.id,
            defaults={
                'name': '탄소배출권 대표 상품',
                'content_type': content_type
            }
        )
        print(f"Carbon SpotProduct {'created' if created else 'already exists'}: ID {spot_product.id}")
    else:
        print("Carbon 데이터가 없습니다.")

def create_all_spot_products():
    create_spot_product_from_gold()
    create_spot_product_from_oil()
    create_spot_product_from_carbon()