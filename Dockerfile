FROM python:3.12.4

ENV PYTHONUNBUFFERED 1

<<<<<<< HEAD
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "logicPuzzle.wsgi:application"]
=======
>>>>>>> f3f07d4aaf9b8d04c7fc7f30a7bcb65d851258d2
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8080
<<<<<<< HEAD
>>>>>>> 50ec3df6b7ce62d40ca67e13bb67da7fb073fd1e
=======
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "logicPuzzle.wsgi:application"]
>>>>>>> f3f07d4aaf9b8d04c7fc7f30a7bcb65d851258d2
