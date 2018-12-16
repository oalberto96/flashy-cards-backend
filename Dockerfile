FROM python:3
MAINTAINER oalberto96
WORKDIR /usr/src/app
COPY . /usr/src/app
EXPOSE 8000
RUN pip install -r requirements.txt
RUN python src/./manage.py migrate
RUN python src/./manage.py loaddata seeder
ENTRYPOINT ["python", "src/./manage.py", "runserver","0.0.0.0:8000"]
