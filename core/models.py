from mongoengine import Document, StringField

class CarBrand(Document):
    name = StringField(required=True)
    country = StringField()