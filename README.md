# Webapp #

This project is meant to serve as template for new projects.

## Quickstart ##

1. Install dependencies

   ```bash
   (webapp-env)$ pip install -r requirements.txt
   ```

1. Install package

   ```bash
   (webapp-env)$ python setup.py develop
   ```

1. Set up database

   ```bash
   (webapp-env)$ python scripts/create_db.py
   ```

1. Run web server

   ```bash
   (webapp-env)$ python wsgi.py
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

   ```
   $ bower install bootstrap-sass-official
   ```

1. Run frontend build scripts

   ```
   $ grunt build
   ```
