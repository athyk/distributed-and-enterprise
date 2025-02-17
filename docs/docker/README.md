# Docker 

We use docker compose due to using multiple services in the project.

## Running

Ensure docker is installed on your machine.

- Rename `.example.env` to `.env` and fill in the required fields
- Run `docker-compose up --build`.
- After a minute or so after the build is complete, visit http://localhost:8000 in your browser
- To run in the background, run `docker-compose up -d --build`. (add a `-d` flag)

## Docker compose Explained

```yaml
services:
  db:
    image: postgres:17
    ports:
      - ${DATABASE_PORT}:${DATABASE_PORT}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${DATABASE_NAME}
      POSTGRES_USER: ${DATABASE_USERNAME}
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
      POSTGRES_PORT: ${DATABASE_PORT}
    env_file: .env
  minio:
    image: docker.io/bitnami/minio:2025.2.7
    ports:
      - ${MINIO_PORT}:${MINIO_PORT}
      - ${MINIO_CONSOLE_PORT}:${MINIO_CONSOLE_PORT}
    volumes:
      - 'minio_data:/data'
    environment:
      - MINIO_ROOT_USER=${MINIO_ROOT_USER}
      - MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD}
      - MINIO_DEFAULT_BUCKETS=${MINIO_DEFAULT_BUCKETS}
    env_file: .env
  django-backend:
    build: .
    container_name: django-backend
    ports:
      - ${DJANGO_PORT}:8000
    depends_on:
      - db
      - minio
      - redis
    env_file: .env
  svelte-frontend:
    build:
      context: ./frontend
    container_name: svelte-frontend
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - django-backend
    working_dir: /app
  redis:
    image: redis:latest
    ports:
      - ${REDIS_PORT}:${REDIS_PORT}
    env_file: .env
    logging:
      driver: none
volumes:
  postgres_data:
  minio_data:
```

- `db` service: This is the PostgreSQL database service, handles the database like Mysql/Sqlite.
- `minio` service: This is the Minio service, handles file storage similar to AWS S3.
- `django-backend` service: This is the Django service (web server/backend).
- `svelte-frontend` service: This is the Svelte service (frontend).
- `redis` service: This is the Redis service, handles caching.

#### Why use `environment` with `env_file`?
It shows clearly what each service requires and allows for easy configuration.

#### Why use `volumes`?

The volumes of `postgres_data` and `minio_data` are used to store the data of the database and Minio service respectively.
They are stored within the docker directory and are not lost when the container is removed.

This could be tied to a local directory within the project to transfer data and potentially store it in a repository.

#### Why use `depends_on`?
`django-backend` uses `depends_on` to ensure that the database services are up and running before the Django service starts.

`svelte-frontend` uses `depends_on` to ensure that the Django service is up and running before the Svelte service starts.

#### Why use `logging`?
`logging` is used to disable the logging of the services as it can be verbose and unnecessary.

When using `docker-compose up --build`, the logs are shown in the terminal, which having just django logs is more useful.

#### What's the `build` field?

The `build` field is used to build the image from the Dockerfile in the current directory.

[frontend/Dockerfile](../../frontend/Dockerfile) is used to build the Svelte frontend image.
[Dockerfile](../../Dockerfile) is used to build the Django backend image.


#### What's the `container_name` field?

The `container_name` field is used to give the container a name, which can be used to refer to the container.

## Dockerfile Explained

Both are nearly the same, but the `prod` image is used for production.

See below:
```dockerfile
FROM python:3.13-slim AS base

RUN mkdir /app
WORKDIR /app

# Prevents writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

# Copy the project files and install the dependencies
COPY requirements.txt  /app/
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim AS prod

# Create a non-root user
RUN useradd -r appuser && mkdir /app && chown -R appuser /app

COPY --from=base /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

WORKDIR /app
COPY --chown=appuser:appuser . .

# Prevents writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "unihub_project.wsgi:application"]
```

- Using 3.13 as the python version, and `-slim` to reduce the size of the image. 
- It creates a directory at `/app` and sets it as the working directory, so that if you navigate to the container, you are in the `/app` directory.
- It prevents writing pyc files to disk.
- Upgrades pip (python package manager) to the latest version. And then installs the requirements from the `requirements.txt` file.
- Then creates a new container, taking all the installed packages from the `base` container, and copies the project files into the container.
- Creates a non-root user, for security to prevent running the container as root, and sets the working directory to `/app`.
- Prevents writing pyc files to disk.
- Exposes port 8000 and runs the gunicorn server. Gunicorn was chosen as Athy believes it's fastest.

## Docker Compose Commands

```bash
docker compose up --build
```
This command builds the images and starts the containers.

```bash
docker compose up -d --build
```
This command builds the images and starts the containers in the background. (add a `-d` flag)

```bash
docker compose down
```
This command stops and removes the containers. If you used `-d` flag, you can use `docker-compose down` to stop the containers.