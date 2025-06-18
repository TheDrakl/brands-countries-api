import json
import os
import django
from collections import defaultdict
from core.models import Country, State, City

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

with open("core/scripts/countries+states+cities.json", "r") as file:
    data = json.load(file)

existing_countries = {c.name: c for c in Country.objects.only("name")}
existing_states = defaultdict(dict)
for state in State.objects.only("name", "country"):
    existing_states[state.country.id][state.name] = state

existing_cities = defaultdict(dict)
for city in City.objects.only("name", "state"):
    existing_cities[city.state.id][city.name] = city

new_countries = []
new_states = []
new_cities = []

for country_item in data:
    country = existing_countries.get(country_item["name"])
    if not country:
        country = Country(
            name=country_item["name"],
            iso2=country_item["iso2"]
        )
        new_countries.append(country)
    for state_item in country_item.get("states", []):
        if country.id:
            state_exists = existing_states[country.id].get(state_item["name"])
        else:
            state_exists = False
        if not state_exists:
            state = State(
                name=state_item["name"],
                state_code=state_item.get("state_code"),
                country=country
            )
            new_states.append(state)
        else:
            state = state_exists
        for city_item in state_item.get("cities", []):
            if state.id:
                city_exists = existing_cities[state.id].get(city_item["name"])
            else:
                city_exists = False
            if not city_exists:
                city = City(
                    name=city_item["name"],
                    state=state,
                    country=country
                )
                new_cities.append(city)

if new_countries:
    Country.objects.insert(new_countries, load_bulk=False)
    print(f"Inserted {len(new_countries)} new countries")

if new_states:
    State.objects.insert(new_states, load_bulk=False)
    print(f"Inserted {len(new_states)} new states")

if new_cities:
    City.objects.insert(new_cities, load_bulk=False)
    print(f"Inserted {len(new_cities)} new cities")