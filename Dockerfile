FROM python:3.12.4

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "logicPuzzle.wsgi:application"]