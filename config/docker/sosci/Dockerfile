FROM alpine:latest

# Initialize
RUN mkdir -p /data/sosci

WORKDIR /data/sosci

COPY ./requirements.txt /data/sosci/

# Setup
RUN apk update
RUN apk upgrade
RUN apk add --update python3 python3-dev postgresql-client postgresql-dev build-base gettext zlib1g-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Clean
RUN apk del -r python3-dev postgresql

# Prepare
# copy project to working directory in image
COPY . /data/sosci/

# RUN python3 manage.py collectstatic

# RUN python3 manage.py makemigrations

# RUN python3 manage.py migrate