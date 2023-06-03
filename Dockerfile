FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /harrypotter
WORKDIR /harrypotter
COPY requeriments.txt /harrypotter/
RUN pip install -r requeriments.txt
COPY . /harrypotter/
CMD python manage.py runserver 0.0.0.0:5080
