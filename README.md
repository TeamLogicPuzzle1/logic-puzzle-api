# logic-puzzle-server

## 도커 실행
###  - 도커 이미지 빌드 : docker build -t test-image .

### - 도커 run : docker run -d -p 8080:8080 test-image:latest

### redis 로컬 서버 실행 : docker run -d -p 6379:6379 redis

## 도커 컴포즈 실행
### 1. docker-compose up -d --build

## 도커 컴포즈 재실행
### 1. docker-compose down

### 2. docker-compose up -d --build
