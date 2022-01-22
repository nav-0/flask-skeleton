# en-passant-flask-skeleton
A skeleton flask API to do an en passant capture. 

# Install

This skeleton code can be used for:
* RESTful API Server
* Python Client class (to call a remote API server)
* Command line POSIX program (to call remote APIs and do operations locally)
* Command line client (to call a remote API server)
* Python library (to call remote APIs and do operations locally)

## API Install

Use the Dockerfile or docker-compose, use the `dev.env` template to make your `.env`

Running the container will start an API on port 8080

`./rundmc` will handle starting the container

## Python Client
* `pip install -U .`
* `from en_passant.client import Client`

## Command Line Install
* `pip install -U .`
* `en_passant_cli -h` query remote APIs and do operations locally
* `en_passant_client -h` query remote En Passant API

## Library
* `pip install -U -e .[dev]`
* `export PASSANT_FLASK+DEBUG=true`
* `en_passant_api` run API locally for testing
* Visit the API Swagger UI at `scheme://host:port/en/api/v1.0/passant/apidocs`


