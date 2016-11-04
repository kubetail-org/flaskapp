# Flask Seed App

[![Requirements Status](https://requires.io/github/muicss/flaskapp/requirements.svg?branch=master)](https://requires.io/github/muicss/flaskapp/requirements/?branch=master)
[![devDependency Status](https://david-dm.org/muicss/flaskapp/dev-status.svg?path=static-src)](https://david-dm.org/muicss/flaskapp?path=static-src#info=devDependencies)

This app is meant to serve as template for new projects. It has the following features:

  * User accounts implemented with SQLite, cookies and Flask-Login
  * Passwords hashed with bcrypt
  * CSRF protection with Flask-CSRF
  * Email with Flask-Mail
  * Login/logout/forgot password workflow
  * Static asset build step with gulp
  * Basic HTML Web and Email templates with MUI (https://www.muicss.com)
  * Unittests

To create a new app from `flaskapp` first clone the repository and remove the `.git` directory:

```bash
$ git clone git@github.com:muicss/flaskapp.git
$ rm -rf flaskapp/.git
```

Then, do a search-replace on the string `flaskapp` (remember to replace `<name>` with your app's name):

```bash
$ find flaskapp -type f | xargs sed -i'' -e 's/flaskapp/<name>/g'
$ find flaskapp -type f | xargs sed -i'' -e 's/Flaskapp/<Name>/g'
$ mv flaskapp <name>
$ mv <name>/flaskapp <name>/<name>
```

Now you have your own flask seed project.

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

To work in a sandboxed Python environment we recommend installing the app in a Python [virtualenv](https://pypi.python.org/pypi/virtualenv).

1. Install dependencies

    ```bash
    $ cd /path/to/flaskapp
    $ pip install -r requirements.txt
    ```

1. Setup a SQLite database for development (`app.db`)

   ```bash
   $ python scripts/create_db.py
   ```

1. Environment variables

   In order to configure flaskapp it is recommended that you create an environment file with the required variables listed above:
   
   ```bash
   #!/bin/bash
   # Environment variables for Flask seed app
   
   export DEBUG="True"
   export SECRET_KEY="replaceme"
   export MAIL_PORT="587"
   export MAIL_SERVER="mail.google.com"
   export MAIL_USERNAME="user@example.com"
   export MAIL_PASSWORD="replaceme"
   ```
   
   To add the variables to your environment you can source the file as part of your normal workflow:
   
   ```bash
   $ source /path/to/env-vars.sh
   ```

1. Run development server

   ```bash
   $ python wsgi.py
   ```

   View at http://127.0.0.1:5000

1. Frontend build scripts

   Install node dependencies:

   ```bash
   $ cd /path/to/flaskapp/static-src
   $ npm install
   ```

   Run gulp:

   ```bash
   $ ./node_modules/.bin/gulp build
   ```

## Unittests ##

To run all tests:

```bash
$ nosetests
```

To run an individual test:

```bash
$ nosetests tests/views/test_content.py
```

## Contribute ##

Contributions are welcome! If you'd like to report an issue or submit a pull request please use our github page: https://github.com/muicss/flaskapp.

