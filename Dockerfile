FROM python:3-onbuild
MAINTAINER Maru Berezin

ENV FIUBAR_SECRET_FILE config/secret.json

COPY start.sh /start.sh

EXPOSE 8000

CMD ["/start.sh"]
