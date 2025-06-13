import json
import os
import django
from ..models import CarBrand

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

with open("core/scripts/car_brands.json", "r") as file:
    data = json.load(file)

for item in data:
    brand = CarBrand.objects(name=item["name"]).first()
    if not brand:
        brand = CarBrand(name=item["name"], country=item["country"])
        brand.save()
        print(f"Added brand: {brand.name}")
    else:
        print(f"Brand already exists: {brand.name}")