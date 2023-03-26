## Tech check

This development is based on the KIS (keep it simple) principle.
It is a simple API for obtaining, adding and editing data without applying logic in the process or use third parties in
the process.

### Swagger DOC

You can visit swagger doc at http://127.0.0.1:5000/api/docs/ (when server from docker or local is running)

### Notes to reviewer

Docker is build as a multistage builder and runner.

Builder must build a distributable package with the api (a whl file). In some architectures this cuold be send to nexus
ór another artefacts servers like devpy or pypi for later use in development process.

Runner must get only de whl file (in this case from builder) and install and run it the only requirement to run in flask
is to set the FLASK_APP=api as api is the name of the package.

Multistage schema has also the advantage that if you publish the docker image to docker.io ó AWS ECR or Harbor your
original code could not be present on any docker slide if you compile de wheel with specific parameters only compiled
versions of your files are distributed in runner image.

Docker run application with gunicorn as is recommended way for production environments. Also creates a docker user and
and run werver within for security reasons about docker containers.

Scripts are also packaged inside flask application package as CLI commands in group script.

After run the aplication and generated_data and load_data scripts you can review all persisted data (CSVs and SQLite
database) in ./generated directory

### Run in docker

To run in docker you need docker and docker compose installed on your machine

BUild

```
$ docker compose build
```

Up and running

```
$ docker compose up -d
```

To run generate data script run (with server running)

```
$ docker compose exec api flask script generate_data
```

To run load data script run (with server running)

```
$ docker compose exec api flask script load_data
```

To stop running server run

```
$ docker compose down
```

### Local development

Local config, a virtualenv is recommended.

Install all requirements:

```
$ python3 -m pip install -e .
```

Server up:

```
$ flask run
```

To run generate data script run

```
$ flask script generate_data
```

To run load data script use other console at the same root directory and run (with server running)

```
$ flask script load_data
```

Change models and create new migrations:

```
$ flask db migrate -m '<migration name>'
```
