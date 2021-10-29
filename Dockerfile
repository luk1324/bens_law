FROM python:3.7-slim as production

ENV PYTHONUNBUFFERED=1
WORKDIR /app/

RUN apt-get update && \
    apt-get install -y \
    bash \
    build-essential \
    gcc \
    libffi-dev \
    musl-dev \
    openssl \
    postgresql \
    libpq-dev 


COPY requirements/prod.txt ./requirements/prod.txt

RUN pip install -r ./requirements/prod.txt

COPY manage.py ./manage.py
COPY benford_law ./benford_law

EXPOSE 8000

FROM production

COPY requirements/dev.txt ./requirements/dev.txt
RUN pip install -r ./requirements/dev.txt

COPY . .

CMD python manage.py runserver 0.0.0.0:8000


