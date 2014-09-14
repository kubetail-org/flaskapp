# Webapp

This project is meant to serve as template for new projects.

## Config Variables

webapp can be configured using the following environment variables:

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
    $ virtualenv --distribute webapp-env
    $ cd webapp-env
    $ source bin/activate
    (webapp-env)$ git clone git@github.com:errorpage/webapp.git src/webapp
   ```

1. Install dependencies

   ```bash
   (webapp-env)$ cd src/webapp
   (webapp-env)$ pip install -r requirements.txt
   ```

1. Setup database

   ```bash
   (webapp-env)$ python scripts/create_db.py
   ```

1. Environment variables

   In order to configure webapp it is recommended that you create an environment file with the required variables listed above. To add the variables to your environment you can source the file as part of your normal workflow:

   ```bash
   (webapp-env)$ source /path/to/env-vars.sh
   ```

1. Run unittests

    ```bash
    (webapp-env)$ nosetests
    ```

1. Run development server

   ```bash
   (webapp-env)$ python wsgi.py
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
(webapp-env)$ nosetests
```

To run an individual test:

```bash
(webapp-env)$ nosetests tests/views/test_content.py
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
