FROM python:3
MAINTAINER oalberto96
WORKDIR /usr/src
COPY requirements.txt /usr/src
RUN pip install -r requirements.txt
VOLUME [ "/user/src/app" ]
WORKDIR /usr/src/app
EXPOSE 8000
ENTRYPOINT ["python", "src/./manage.py", "runserver","0.0.0.0:8000"]
