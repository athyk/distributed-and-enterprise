# DeSD UniHub

## Running

Ensure docker is installed on your machine.

- Rename `.example.env` to `.env` and fill in the required fields
- Run `docker-compose up --build`.
- Visit http://127.0.0.1:8000 in your browser when the build is complete.

To run in the background, run `docker-compose up -d --build`.


## Creating the project

First command was: `django-admin startproject unihub_project .`

## Need help or need to know more?

See the documentation written at [`/docs/README.md`](/docs) for more information.

## Backend Testing

Run the following (**on unix/linux only**) to run the backend tests:

```shell
PYTHONPATH=$(pwd)/backend/common/proto  && coverage run -m unittest discover backend/tests  && coverage report
```