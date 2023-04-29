FROM python:3.11-slim-buster

WORKDIR /Perergine

COPY . /Perergine

RUN pip install --no-cache-dir -r requirements.txt

# RUN apt-get update && apt-get install -y default-libmysqlclient-dev
    # pip install --no-cache-dir -r requirements.txt


# RUN apt-get update && \
#     apt-get install -y default-libmysqlclient-dev && \
#     pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=peregrine_project.settings.prod

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

