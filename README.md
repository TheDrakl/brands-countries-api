## Overview
This project is a Django backend that uses MongoDB as its database. It is containerized with Docker and includes a GraphQL API using Graphene. The API provides access to car brands, countries, states, cities, and charging stations data.

## Features
- Django 4.x backend
- MongoDB integration via MongoEngine
- GraphQL API with Graphene and graphene-mongo
- Geospatial queries for charging stations
- Dockerized for easy development and deployment

## Requirements
- Python 3.12+
- Docker & Docker Compose

## Setup

### 1. Clone the repository
```sh
git clone https://github.com/TheDrakl/brands-countries-api/
cd brands-countries-api
```

### 2. Local Development (without Docker)
- Ensure MongoDB is running locally on `localhost:27017`.
- Install dependencies:
  ```sh
  python -m venv env
  source env/bin/activate
  pip install -r requirements.txt
  ```
- Start the server:
  ```sh
  python manage.py runserver
  ```

### 3. Development with Docker
- Build and start the containers:
  ```sh
  docker-compose up --build
  ```
- The Django app will be available at [http://localhost:8000](http://localhost:8000)
- MongoDB will be available at `mongodb://localhost:27017` (from your host) and as `mongodb://mongo:27017` (from within Docker containers).


## Environment Variables
- `MONGO_URI`: MongoDB connection string (default: `mongodb://localhost:27017/greencarlane_backend`)
- `MONGO_DB`: MongoDB database name (default: `greencarlane_backend`)

## Loading Initial Data

This project includes scripts to populate the database with countries, states, cities, car brands, and charging stations.

### 1. Load Countries, States, and Cities

To import all countries, their states, and cities from the provided JSON file, run:

```sh
python -m core.scripts.load_countries
```

This script will:
- Add any new countries, states, and cities from `core/scripts/countries+states+cities.json` that are not already in the database.

### 2. Load Car Brands

To import car brands from the provided JSON file, run:

```sh
python -m core.scripts.load_brands
```

This script will:
- Add any new car brands from `core/scripts/car_brands.json` that are not already in the database.

### 3. Load Charging Stations

To import charging stations from the provided JSON file, run:

```sh
python -m core.scripts.load_charging_stations
```

This script will:
- Add any new charging stations from `core/scripts/charging_stations.json` that are not already in the database.
- Each station includes location data (GeoJSON Point format) for geospatial queries.


## How to use API

After loading data into database and starting server, you can access the GraphQL API at `http://localhost:8000/graphql/`.

### Example Queries

#### Get all car brands:
```graphql
query {
  allCarBrands {
    name
    country
  }
}
```

#### Get all countries:
```graphql
query {
  allCountries {
    name
    iso2
  }
}
```

#### Get states by country name:
```graphql
query {
  allStates(countryName: "United States") {
    name
    stateCode
    country {
      name
    }
  }
}
```

#### Get cities by state:
```graphql
query {
  allCities(stateName: "California") {
    name
    state {
      name
    }
    country {
      name
    }
  }
}
```

#### Find nearest charging stations:
```graphql
query {
  nearestStations(latitude: 40.7128, longitude: -74.0060) {
    name
    address
    location {
      type
      coordinates
    }
    country
    operator
    status
    connections {
      type
      level
      powerKw
      currentType
      quantity
    }
  }
}
```