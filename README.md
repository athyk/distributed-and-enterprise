# DeSD UniHub

## Running

Ensure docker is installed on your machine.

- Rename `.example.env` to `.env` and fill in the required fields
- Run `docker-compose up --build`.
- Visit http://127.0.0.1:8000 in your browser when the build is complete.

To run in the background, run `docker-compose up -d --build`.

## Need help or need to know more?

See the documentation written at [`/docs/README.md`](/docs) for more information.

## Backend Testing

Run the following (**on unix/linux only**) to run the backend tests:

```shell
PYTHONPATH=$(pwd)/backend/common/proto  && coverage run -m unittest discover backend/tests && coverage report
```

## Where things are

Our code is located in this GitHub Repo. Link: https://github.com/athyk/distributed-and-enterprise

There are 9 containers in total for this project
- 1 Frontend container
- 8 Backend containers

The only container that will be exposed to the internet will be the django-backend container.
All other containers are internal systems.

All Django views are located in this directory.
[`./backend/core/view`](backend/core/view)

All backend container directories arelocated within `./backend/<container_name>`, where a container name of `accounts` leads to the account service.

The common directory [`./backend/common`](backend/common) contains 
all the files and functions that are used to support the use of multiple containers/services.

Redis is used for session management in the application.
This was chosen over JWT as there isn't a use case for stateless tokens reducing complexity. 
For a secure use of JWTs, refresh and access tokens would need to be created and managed, drastically increasing complexity.

Sessions improve security as they can be revoked server-side through a logout from everywhere function, 
they are also up to date as user information is fetched whenever requested.

## How the routes are structured

From the frontend container to the core container (django-backend) a HTTP based REST request is used to fetch data.
The core container then uses gRPC to request the data from the container(s) that need to be contacted.

This is done for two reasons:
- The setup for a gRPC server and communications are defined within a ProtoBuf file (.proto) and for a structured approach
- Communicating to a gRPC server, the languages between the sender and receiver can be different but remain type safe
  - A request in Python can send a request to a go/rust/C++ server while keeping the original type used.
  - It is easy to refactor an individual container whilst using the most suitable language for its intended operations
  - It is performant, faster than REST, [25-30% faster](docs/microservices)
