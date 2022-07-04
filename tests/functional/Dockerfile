FROM python:3.9.12-alpine3.14

RUN apk update \
    && apk add build-base

COPY requirements.txt .

RUN pip install -U setuptools pip
COPY . .
RUN pip install -r requirements.txt

ENV PYTHONPATH=${PYTHONPATH}:/functional
#CMD ["python3", "./src/load_data_for_test.py"]
CMD ["pytest", "./src/"]