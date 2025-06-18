from mongoengine import Document, StringField, ReferenceField


class CarBrand(Document):
    name = StringField(required=True)
    country = StringField()


class Country(Document):
    name = StringField(required=True, unique=True)
    iso2 = StringField()


class State(Document):
    name = StringField(required=True)
    state_code = StringField()
    country = ReferenceField(Country, required=True)


class City(Document):
    name = StringField(required=True)
    state = ReferenceField(State, required=True)
    country = ReferenceField(Country, required=True)
