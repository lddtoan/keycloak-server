# Keycloak Dev

Keycloak for development.

# Requirement

- Docker 23.0.2
- Python 3.10.6

## Setup

Copy `.env.example` to `.env` and update values

Allow execute `run`

```
chmod u+x run
```

## Run

Build and run container

```
./run
```

Visit `http://<keycloak-server>/realms/<realm>/account` to login or register.
