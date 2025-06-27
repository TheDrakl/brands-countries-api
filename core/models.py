from mongoengine import Document, StringField, ReferenceField, FloatField, BooleanField, DateTimeField, IntField, EmbeddedDocumentListField, EmbeddedDocument, PointField


class CarBrand(Document):
    name = StringField(required=True)
    country = StringField()


class Country(Document):
    name = StringField(required=True, unique=True)
    iso2 = StringField()
    
    meta = {
        'indexes': [
            'name',
            'iso2'
        ]
    }


class State(Document):
    name = StringField(required=True)
    state_code = StringField()
    country = ReferenceField(Country, required=True)
    
    meta = {
        'indexes': [
            'name',
            'state_code',
            'country'
        ]
    }


class City(Document):
    name = StringField(required=True)
    state = ReferenceField(State, required=True)
    country = ReferenceField(Country, required=True)
    
    meta = {
        'indexes': [
            'name',
            'state',
            'country'
        ]
    }

class Connection(EmbeddedDocument):
    type = StringField()
    level = StringField()
    power_kw = FloatField()
    current_type = StringField()
    quantity = IntField()

class ChargingStation(Document):
    external_id = StringField(required=True, unique=True)
    name = StringField(required=True)
    address = StringField()
    location = PointField(required=True)
    country = StringField()
    operator = StringField()
    status = StringField()
    access = StringField()
    usage_cost = StringField()
    total_plugs = IntField()
    available = BooleanField()
    last_verified = DateTimeField()
    last_updated = DateTimeField()
    connections = EmbeddedDocumentListField(Connection)

    meta = {
            'collection': 'charging_stations',
            'indexes': [
                'external_id',
                'name',
                'country',
                'operator',
                [('location', '2dsphere')]
            ]
        }