# Webapp

This project is meant to serve as template for new projects.

## Config Variables

flaskapp can be configured using the following environment variables:

Name          | Description                 | Default | Required
------------- | --------------------------- | ------- | -------
DEBUG         | Flask debug variable        | "False" | no
SECRET_KEY    | Flask cookie encryption key | null    | yes
MAIL_PORT     | SMTP port                   | null    | yes
MAIL_SERVER   | SMTP hostname               | null    | yes
MAIL_USERNAME | SMTP username               | null    | yes
MAIL_PASSWORD | SMTP password               | null    | yes

## Quickstart

1. Create virtual environment, checkout repository

    ```bash
    $ virtualenv --distribute flaskapp-env
    $ cd flaskapp-env
    $ source bin/activate
    (flaskapp-env)$ git clone git@github.com:errorpage/flaskapp.git src/flaskapp
   ```

1. Install dependencies

   ```bash
   (flaskapp-env)$ cd src/flaskapp
   (flaskapp-env)$ pip install -r requirements.txt
   ```

1. Setup database

   ```bash
   (flaskapp-env)$ python scripts/create_db.py
   ```

1. Environment variables

   In order to configure flaskapp it is recommended that you create an environment file with the required variables listed above. To add the variables to your environment you can source the file as part of your normal workflow:

   ```bash
   (flaskapp-env)$ source /path/to/env-vars.sh
   ```

1. Run unittests

    ```bash
    (flaskapp-env)$ nosetests
    ```

1. Run development server

   ```bash
   (flaskapp-env)$ python wsgi.py
   ```

   View at http://127.0.0.1:5000

1. Frontend build scripts

   Install node dependencies using npm:

   ```bash
   $ cd scripts/frontend
   $ npm install
   ```

   Run grunt:

   ```bash
   $ grunt build
   ```

## Unittests ##

To run all tests:

```bash
(flaskapp-env)$ nosetests
```

To run an individual test:

```bash
(flaskapp-env)$ nosetests tests/views/test_content.py
```

## Development ##

Dependencies:

 - nodejs
 - npm
 - Bower (http://bower.io/)

1. Install nodejs dependencies

   ```bash
   $ npm install
   ```

1. Install bootstrap-sass-official

   ```bash
   $ bower install bootstrap-sass-official
   ```

1. Run frontend build scripts

   ```bash
   $ grunt build
   ```
