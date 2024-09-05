FROM python:3.12.4

ENV PYTHONUNBUFFERED 1
#
#WORKDIR /usr/src/app
#
#COPY . ./
#
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
#
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
#
#EXPOSE 8080

RUN pip install --no-cache-dir uwsgi

RUN pip3 install django

RUN mkdir /srv/logicpuzzle_web

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["uwsgi", "--ini", "uwsgi/uwsgi.ini"]

EXPOSE 8080

