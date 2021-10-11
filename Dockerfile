FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /vol/web/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD uwsgi --ini uwsgi.ini