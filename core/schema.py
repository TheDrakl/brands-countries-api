import graphene
from graphene_mongo import MongoengineObjectType
from .models import CarBrand, Country, State, City

class CarBrandType(MongoengineObjectType):
    class Meta:
        model = CarBrand

class CountryType(MongoengineObjectType):
    class Meta:
        model = Country

class StateType(MongoengineObjectType):
    class Meta:
        model = State

class CityType(MongoengineObjectType):
    class Meta:
        model = City

class Query(graphene.ObjectType):
    all_car_brands = graphene.List(CarBrandType)
    all_countries = graphene.List(CountryType)
    all_states = graphene.List(
        StateType, country_name=graphene.String(), country_id=graphene.ID()
    )
    all_cities = graphene.List(
        CityType,
        country_name=graphene.String(),
        country_id=graphene.ID(),
        state_name=graphene.String(),
        state_id=graphene.ID(),
    )

    def resolve_all_car_brands(root, info):
        return CarBrand.objects.all()

    def resolve_all_countries(root, info):
        return Country.objects.all()

    def resolve_all_states(root, info, country_name=None, country_id=None):
        if country_id:
            return State.objects.filter(country=country_id)
        if country_name:
            country = Country.objects(name=country_name).first()
            if country:
                return State.objects.filter(country=country)
            else:
                return []
        return State.objects.all()

    def resolve_all_cities(
        root, info, country_name=None, country_id=None, state_name=None, state_id=None
    ):
        if state_id:
            return City.objects.filter(state=state_id)
        if state_name:
            state = State.objects.filter(name=state_name).first()
            if state:
                return City.objects.filter(state=state)
            else:
                return []
        if country_id:
            return City.objects.filter(country=country_id)
        if country_name:
            country = Country.objects.filter(name=country_name).first()
            if country:
                return City.objects.filter(country=country)
            else:
                return []
        return City.objects.all()

schema = graphene.Schema(query=Query)