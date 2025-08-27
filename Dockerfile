FROM python:3.11-slim

WORKDIR /home/bikeshareapp

COPY ec2_requirements.txt .

RUN apt-get update && \
    apt-get install -y \
    python3-dev \
    libmariadb-dev \
    libmariadb-dev-compat \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r ec2_requirements.txt
RUN pip install gunicorn

COPY machine_learning/trained_model/ machine_learning/trained_model/
COPY web/ web/

ENV GUNICORN_WORKERS=1
CMD ["sh", "-c", "gunicorn --workers=${GUNICORN_WORKERS} --bind=0.0.0.0:5000 web.gunicorn:app"]