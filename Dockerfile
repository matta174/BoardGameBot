FROM python:3.6-alpine

ENV DOCKER_CONTAINER Yes

COPY requirements.txt .

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 apt-get update && \
 apt-get -y install gcc mono-mcs && \
 rm -rf /var/lib/apt/lists/* && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . .

CMD [ "python", "./main.py" ]
