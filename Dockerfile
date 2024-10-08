FROM python:3.12.4

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "logicPuzzle.wsgi:application"]
WORKDIR /usr/src/app

COPY . ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

EXPOSE 8080
>>>>>>> 50ec3df6b7ce62d40ca67e13bb67da7fb073fd1e
