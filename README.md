# Parking Lot Management

Backend Service for a Parking Lot.

## Tech Stack

**Framework:** [Django](https://www.djangoproject.com/) with [Rest Framework](https://www.django-rest-framework.org/)

**Database:** PostgreSQL

## Installation and Usage

- Create conda environment and install python

  ```bash
  conda create -n parking
  conda activate parking
  conda install python=3.10.4
  ```

- Install dependencies

  ```bash
  pip install -r requirements.txt --no-cache
  ```

- Host Postgres Database using Docker

  ```bash
  sudo docker run --network=host --name parking-lot -e POSTGRES_DB=parking -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -d postgres
  ```

  - Database Name: parking
  - User: postgres
  - Password: postgres
  - Host: 127.0.0.1 (localhost)
  - Port: 5432

- Migrate and Run the server
  ```bash
  python manage.py migrate
  python manage.py runserver
  ```
