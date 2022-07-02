FROM python:3.9.12-alpine3.14

RUN apk update \
    && apk add build-base

COPY requirements.txt .

RUN pip install -U setuptools pip
COPY . .
RUN pip install -r requirements.txt \
    && chmod +x ./utils/redis_elastic_waiter.sh

ENV PYTHONPATH=${PYTHONPATH}:/functional

ENTRYPOINT ["/utils/redis_elastic_waiter.sh"]

CMD ["pytest", "./src/"]