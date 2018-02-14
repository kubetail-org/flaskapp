FROM python:2.7.14-alpine
MAINTAINER Andres Morey "andresmarcel@gmail.com"

# add app
COPY . /app
WORKDIR /app

# install system dependencies
RUN apk update
RUN apk add gcc libffi-dev libxml2-dev libxslt-dev musl-dev

# upgrade pip
RUN pip install -U pip

# install app
RUN pip install -r requirements.txt

# entrypoint
ENTRYPOINT ["gunicorn", "wsgi:app"]
CMD ["--bind=0.0.0.0:5000", "--worker-class=gevent", "--workers=4", "--threads=1", "--preload"]
