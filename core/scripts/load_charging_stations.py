import os
import json
import django
from ..models import ChargingStation, Connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

with open("core/scripts/charging_stations.json", "r", encoding="utf-8") as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON decode error at line {e.lineno}, column {e.colno}")
        data = []

existing_stations = {s.external_id: s for s in ChargingStation.objects.only("external_id")}

new_stations = []

for station_data in data:
    if station_data["external_id"] in existing_stations:
        continue

    connections_data = station_data.pop("connections", [])
    connection_objs = [Connection(**conn) for conn in connections_data]

    latitude = station_data.pop("latitude", None)
    longitude = station_data.pop("longitude", None)

    station = ChargingStation(**station_data)
    if latitude and longitude:
        station.location = [longitude, latitude]

    station.connections = connection_objs
    new_stations.append(station)

if new_stations:
    ChargingStation.objects.insert(new_stations, load_bulk=False)
    print(f"Inserted {len(new_stations)} new stations")
else:
    print("No new stations were inserted.")