FROM python:3.8.2-alpine as base
MAINTAINER Andres Morey "andresmarcel@gmail.com"

# -----------------------------------------------------------------------------

FROM base as builder

# system dependencies
RUN apk update \
    && apk add --no-cache --virtual build-dependencies gcc libffi-dev libxml2-dev musl-dev make \
    && apk add --no-cache libxslt-dev \
    && apk add --no-cache bash

# python dependencies
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# cleanup /usr/lib
RUN apk del build-dependencies

# -----------------------------------------------------------------------------

FROM base

# copy dependencies
COPY --from=builder /usr/lib /usr/lib
COPY --from=builder /usr/local /usr/local

# copy source
COPY . /app
WORKDIR /app

# entrypoint
ENTRYPOINT ["gunicorn", "wsgi:app"]
CMD ["--bind=0.0.0.0:5000", "--worker-class=gevent", "--workers=4", "--threads=1", "--preload"]
