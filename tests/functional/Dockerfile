FROM python:3.9.12-alpine3.14

RUN apk update \
    && apk add build-base

COPY requirements.txt .

RUN pip install -U setuptools pip
COPY . .
RUN pip install -r requirements.txt

CMD ["pytest", "./src/"]