FROM python:3-alpine
ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install uwsgi

EXPOSE 8000

CMD ["/app/scripts/runner.sh"]