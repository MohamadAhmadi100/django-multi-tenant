#FROM python:3.9-slim-buster
#
#RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
#COPY nginx.default /etc/nginx/sites-available/default
#RUN ln -sf /dev/stdout /var/log/nginx/access.log \
#    && ln -sf /dev/stderr /var/log/nginx/error.log
#
#RUN mkdir -p /opt/app
#COPY entrypoint.sh /opt/app/
#COPY ./requirements.txt /opt/app/
#COPY . /opt/app/
#WORKDIR /opt/app
#RUN pip install -r requirements.txt
#RUN chown -R www-data:www-data /opt/app
#
#RUN chmod +x /opt/app/entrypoint.sh
#
#EXPOSE 8000
## run entrypoint.sh
#CMD ["/opt/app/entrypoint.sh"]

###########
# BUILDER #
###########

# pull official base image
FROM python:3.9-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y dist-upgrade && apt-get install -y gcc && apt install -y netcat
RUN apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.9-slim-buster

# create directory for the app user
RUN mkdir -p /home/app
ENV HOME=/home/app
ENV APP_HOME=/home/app/spov
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/media
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/logs
WORKDIR $APP_HOME

# install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME
COPY static $APP_HOME
COPY .env $APP_HOME/.env

#RUN apt-get update && apt-get -y dist-upgrade
#RUN apt-get install -y netcat

RUN chmod +x /home/app/spov/entrypoint.sh
# run entrypoint.sh
ENTRYPOINT ["/home/app/spov/entrypoint.sh"]
