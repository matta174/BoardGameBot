FROM python:3.6-alpine

ADD main.py /

RUN pip install discord

RUN pip install boardgamegeek2

RUN pip install google-api-python-client

CMD [ "python", "./main.py" ]
