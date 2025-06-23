## Overview
This project is a Django backend that uses MongoDB as its database. It is containerized with Docker and includes a GraphQL API using Graphene.

## Features
- Django 4.x backend
- MongoDB integration via MongoEngine
- GraphQL API with Graphene and graphene-mongo
- Dockerized for easy development and deployment

## Requirements
- Python 3.12+
- Docker & Docker Compose

## Setup

### 1. Clone the repository
```sh
git clone https://github.com/TheDrakl/brands-countries-api/
cd backend
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
- `MONGO_URI`: MongoDB connection string (default: `mongodb://localhost:27017/brands-countries-api`)
- `MONGO_DB`: MongoDB database name (default: `brands-countries-api`)

## Loading Initial Data

This project includes scripts to populate the database with countries, states, cities, and car brands.

### 1. Load Countries, States, and Cities

To import all countries, their states, and cities from the provided JSON file, run:

```sh
python core/scripts/load_countries.py
```

This script will:
- Add any new countries, states, and cities from `core/scripts/countries+states+cities.json` that are not already in the database.

### 2. Load Car Brands

To import car brands from the provided JSON file, run:

```sh
python core/scripts/load_brands.py
```

This script will:
- Add any new car brands from `core/scripts/car_brands.json` that are not already in the database.
