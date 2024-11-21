FROM python:3.12.4

# 환경 변수 설정
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# 의존성 설치
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --root-user-action=ignore

# 소스 코드 복사
COPY . ./

# 포트 노출
EXPOSE 8080

# 애플리케이션 실행 명령어
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "logicPuzzle.wsgi:application"]
