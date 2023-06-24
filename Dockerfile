FROM python:3.9-slim-buster

RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir -p /opt/app
COPY entrypoint.sh /opt/app/
COPY ./requirements.txt /opt/app/
COPY . /opt/app/
WORKDIR /opt/app
RUN pip install -r requirements.txt
RUN chown -R www-data:www-data /opt/app

RUN chmod +x /opt/app/entrypoint.sh

EXPOSE 8000
# run entrypoint.sh
CMD ["/opt/app/entrypoint.sh"]