# BUILD IMAGE
FROM python:3.11 as build-python
MAINTAINER Titov Anton <webdev@titovanton.com>

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python-dev
RUN apt-get install -y python-setuptools

RUN pip install --upgrade pip

# For better Docker caching purpose
RUN pip install "fastapi[all]"
RUN pip install psycopg2-binary
RUN pip install SQLAlchemy==2.0.12
RUN pip install alembic==1.10.4
RUN pip install boto3==1.26.124
RUN pip install pytest==7.3.1
RUN pip install sqlalchemy-utils==0.41.1
RUN pip install Faker==18.6.2

# -----------------------------------------------------
# RUN IMAGE
FROM python:3.11-slim
MAINTAINER Titov Anton <webdev@titovanton.com>

RUN groupadd -r docker -g 1000 && \
   useradd -m -r -g docker -u 1000 docker && \
   echo "docker:docker" | chpasswd && adduser docker sudo

COPY --from=build-python \
   /usr/local/lib/python3.11/site-packages/ \
   /usr/local/lib/python3.11/site-packages/
COPY --from=build-python \
   /usr/local/bin/ \
   /usr/local/bin/

WORKDIR /app
RUN mkdir aliases
COPY aliases ./
COPY src ./

RUN echo "for fl in /app/aliases/*.sh; do source \$fl; done" >> /home/# docker/.bashrc
