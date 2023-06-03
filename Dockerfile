FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /harrypotter
WORKDIR /harrypotter
COPY requirements.txt /harrypotter/
RUN pip install -r requirements.txt
COPY . /harrypotter/
CMD python manage.py runserver 0.0.0.0:8080
