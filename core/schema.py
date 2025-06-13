import graphene
from graphene_mongo import MongoengineObjectType
from .models import CarBrand

class CarBrandType(MongoengineObjectType):
    class Meta:
        model = CarBrand

class Query(graphene.ObjectType):
    all_car_brands = graphene.List(CarBrandType)

    def resolve_all_car_brands(root, info):
        return CarBrand.objects.all()

schema = graphene.Schema(query=Query)