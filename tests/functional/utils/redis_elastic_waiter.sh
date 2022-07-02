#!/bin/sh

if [ "$REDIS_DB" = "redis" ]
then
    echo "Waiting for Redis db..."

    while ! nc -z $REDIS_HOST $REDIS_PORT; do
      sleep 0.1
    done

    echo "Redis db started"
fi

if [ "$ELASTIC_DB" = "elastic" ]
then
    echo "Waiting for Elasticsearch db..."

    while ! nc -z $ELASTIC_HOST $ELASTIC_PORT; do
      sleep 0.1
    done

    echo "Elasticsearch db started"
fi

exec "$@"