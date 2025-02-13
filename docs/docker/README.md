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
    logging:
      driver: none
  django-web:
    build: .
    container_name: django-docker
    ports:
      - ${DJANGO_PORT}:8000
    depends_on:
      - db
      - minio
      - redis
    env_file: .env
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
- `django-web` service: This is the Django service (web server).
- `redis` service: This is the Redis service, handles caching.

#### Why use `environment` with `env_file`?
It shows clearly what each service requires and allows for easy configuration.

#### Why use `volumes`?

The volumes of `postgres_data` and `minio_data` are used to store the data of the database and Minio service respectively.
They are stored within the docker directory and are not lost when the container is removed.

This could be tied to a local directory within the project to transfer data and potentially store it in a repository.

#### Why use `depends_on`?
`django-web` uses `depends_on` to ensure that the database services are up and running before the Django service starts.

#### Why use `logging`?
`logging` is used to disable the logging of the services as it can be verbose and unnecessary.

When using `docker-compose up --build`, the logs are shown in the terminal, which having just django logs is more useful.
