import graphene
from graphene_mongo import MongoengineObjectType
from .models import CarBrand, Country, State, City, ChargingStation
import math

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

class ConnectionType(graphene.ObjectType):
    type = graphene.String()
    level = graphene.String()
    power_kw = graphene.Float()
    current_type = graphene.String()
    quantity = graphene.Int()

class ChargingStationType(MongoengineObjectType):
    class Meta:
        model = ChargingStation

    connections = graphene.List(ConnectionType)

    def resolve_connections(parent, info):
        return parent.connections

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
    nearest_stations = graphene.List(
        ChargingStationType,
        latitude=graphene.Float(required=True),
        longitude=graphene.Float(required=True)
    )

    def resolve_all_car_brands(root, info):
        return CarBrand.objects.all()

    def resolve_all_countries(root, info):
        return Country.objects.all()

    def resolve_all_states(root, info, country_name=None, country_id=None):
        if country_id:
            return State.objects.filter(country=country_id).select_related()
        if country_name:
            return State.objects.filter(country__name=country_name).select_related()
        return State.objects.all().select_related()

    def resolve_all_cities(
        root, info, country_name=None, country_id=None, state_name=None, state_id=None
    ):
        if state_id:
            return City.objects.filter(state=state_id).select_related()
        if state_name:
            return City.objects.filter(state__name=state_name).select_related()
        if country_id:
            return City.objects.filter(country=country_id).select_related()
        if country_name:
            return City.objects.filter(country__name=country_name).select_related()
        return City.objects.all().select_related()
    

    def resolve_nearest_stations(root, info, latitude, longitude):
        nearby = ChargingStation.objects(
            location__near=[longitude, latitude]
        ).limit(50)
        
        return list(nearby)

schema = graphene.Schema(query=Query)