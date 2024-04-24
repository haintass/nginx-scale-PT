# nginx-scale-PT

A simple HTTP service that scales horizontally using nginx.


Usage Guide
------------
To run the application you will need `.env` environment variables:
```dotenv
PROJECT_NAME="<Service name>"
VERSION_APP="<Application version number>"
REDIS_URL="<Redis url - redis://username:password@host:port/0>"
```


To start the `server` open cmd, navigate to root project directory and run the following command:
```cmd
docker compose up --build
```
The command will start a server with nginx reverse proxy and `5` application replicas. 
You can change the number of replicas in the docker-compose.yml, in the `deploy` section.

After successful startup, the server will listen for incoming requests at http://0.0.0.0:8100 
(the port can be changed in docker-compose.yml)

Swagger is available at http://0.0.0.0:8100/api/docs#/


## Project structure

* Project root - it contains basic things, for example, docker files, gitignore, config files, etc.
* `src` - contains the application source code.
* `main.py` - the entry point of the application.
* `api` - module in which the API is implemented.
* `core` - contains various configuration files and application settings.
* `db` - provides database objects and providers for dependency injection.
* `schemas` - contains classes that describe business entities.
* `services` - this module contains the implementation of all business logic.