from django.apps import AppConfig
from mongoengine import connect, get_connection
from mongoengine.connection import ConnectionFailure

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        try:
            get_connection()
        except ConnectionFailure:
            connect(db='car_db', host='mongodb://localhost:27017')