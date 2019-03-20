FROM python:3.6-alpine
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /app
WORKDIR /app

CMD [ "python", "./main.py" ]
