FROM python:3-onbuild
MAINTAINER Maru Berezin

EXPOSE 8000

CMD ["./local/start.sh"]
