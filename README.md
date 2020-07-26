# Studio Ghibli Movie List

## About

Python application which serves a page on `localhost:8000/movies/`. This page 
contains a plain list of all movies fetched from the Ghibli REST API. Each 
movie has a list of people that appear in it.


## Dependencies

Service is writen in *Python*. This was an exercise in simplicity, so external 
dependencies are minimized. Third-party libraries used in project:

- [Django](https://www.djangoproject.com/)
- [Requests](http://docs.python-requests.org/en/master/)


## Installation

To install project, create python virtual environment for Python 3.8, activate 
it and install dependencies from root project directory (`/ghibli_task`) with 

`pip install -r requirements.txt`

From the django project directory (`/ghibli_task/ghibli` where `manage.py` is 
located) run migrations with 

`python manage.py migrate` 

Load inital data (URLs and their friendly names) with:

`python manage.py loaddata data_url.json`

Start Django web server with `python manage.py runserver 0.0.0.0:8000`.
Movies list URL is located at `http://0.0.0.0:8000/movies/`.


## Implementation

Application uses two endpoints from 
[Ghibli REST API](https://ghibliapi.herokuapp.com/) 
to collect movies and people. Collected data is stored into database (Sqlite 
is used for sake of simplicity).

From the `/films` endpoint it collects movies and stores it's data, then from 
the `/people` endpoint it collects characters to store them and create 
relations to the movies. Models for representing this data are part of Django 
app `catalog`.

Urls for external API are stored in database (Django app `data_fetcher`) so 
application can track the changes of collected data. First response from 
external API is hashed (with md5) and hash signature is stored for comparing 
with later responses. If later responses are not diferent (have same hash 
signature) application will not process fetched data.


## Caching

Caching logic relies on Django's caching decorator `cache_page`. Local memory 
is used as caching storage. Caching timeout can be adjusted through settings 
constant `CACHE_TIMEOUT_IN_MINUTES` (currently set to 1). Settings file is 
`/ghibli_task/ghibli/ghibli/settings.py`


## Tests

Critical parts of the project are covered with tests and they can be run with:

`python manage.py test`
