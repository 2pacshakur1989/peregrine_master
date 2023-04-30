FROM python:3.11-slim-buster

WORKDIR /Perergine

COPY . . 

# RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y default-libmysqlclient-dev python3-dev build-essential

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=peregrine_project.settings

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

