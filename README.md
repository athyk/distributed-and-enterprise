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

Our code is located in this GitHub Repo.
Link: "https://github.com/athyk/distributed-and-enterprise"

We have 9 containers in total for this project
1 Frontend container
8 Backend containers

The only container that will be exposed to the internet will be the django-backend container.
All other containers are internal systems.

All Django views are located in this directory.
```./backend/core/view```

All backend container directories are structured as follows.
```./backend/container_name```

The common file ```./backend/common``` is the folder that all containers use.
It contains all the files and functions that are used throughout multiple containers.

We use redis for our sessions in the application.
This is handled on the server side which is better than JWT due to the fact that it
reduces complexity and a user only has a session id given to them when they log in.
This keeps all the sensitive data server side inaccessible by others

## How the routes are structured

From the frontend container to the core container (django-backend) we use the typical http request to fetch data
The core container then uses gRPC to request the data from the specified container that needs to be contacted.
This is done for two reasons: -
- gRPC servers only need one file where Django needs multiple to initialise (making it better to manage)
- communicating to a gRPC server, the languages between the sender and receiver can be different
- - this means that a python file can send a request to a go/rust/C++ server with no issues. gRPC handles all the heavy work
- - this makes it easy to adapt a container whilst using the most suitable language for its intended operations
