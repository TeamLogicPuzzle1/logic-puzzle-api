# Project Overview

### LogicPuzzle API 는 음식물 쓰레기 관리와 제품 소비기한 추적을 목적으로 개발되었습니다. 
### 이 프로젝트는 환경 보호와 효율적인 식자재 관리를 돕기 위해 설계되었습니다.

### 주요 기능:
1. **사용자 인증 및 관리**
 - JWT 기반의 안전한 인증 시스템.
 - 회원가입, 로그인, 비밀번호 인증.
2. **제품 관리**
 - OCR 을 통해 제품의 소비기한을 이미지에서 자동으로 추출.
 - 제품 카테고리별 관리 및 필터링.
3. **음식물 쓰레기 통계**
 - 일/주/월별 음식물 쓰레기 데이터 제공.
 - 사용자 맞춤형 통계 제공.
4. **레시피 추천**
 - 사용자가 등록한 제품 데이터를 기반으로 추천 레시피 제공.
5. **알림 시스템**
 - Firebase FCM 을 활용한 알림 기능 (개발 예정).
### 기술 스택:
- **백엔드**: Python 3.10, Django 5.x, Django REST Framework
- **데이터베이스**: MySQL
- **기타**: Docker, Nginx, Firebase, Google Vision API
### 보안 및 인증JWT 인증
- 본 시스템은 **JWT (JSON Web Token)**을 사용하여 사용자를 인증합니다.
- 모든 API 요청은 유효한 JWT 토큰을 통해 인증됩니다.
- 사용자가 로그인하면 JWT 액세스 토큰이 발급되며, 이를 통해 사용자의 권한을
확인합니다.
Google Cloud Vision API 인증 (OAuth2 사용)
- Google Cloud Vision API 는 OAuth2 인증 방식을 사용하여 액세스를 제어합니다.
- oauth2 는 보안성을 강화하고, 인증된 서비스만이 Google Cloud Vision API 에 접근할 수
있도록 합니다.
환경 변수 관리
- 모든 민감한 정보는 env 파일을 사용하여 관리하고, 이 파일은 Git 에 포함되지
않도록 .gitignore 에 추가합니다.
SSL 인증서
-Let's Encrypt 를 사용하여 자동으로 무료 SSL 인증서를 발급받아 HTTPS 로 보안을
강화합니다.
### 개발 환경:
- 운영 체제: Ubuntu 20.04
- 가상화: Docker 컨테이너 기반 개발 및 배포.
- 테스트: Swagger 사용

## Detailed API Documentation

### API: /auth/login
#### **Method:** POST
#### **Description:** 사용자가 로그인하여 JWT 토큰을 발급받습니다.
#### **OperationId:** login
#### **Parameters:**
• - {'name': 'data', 'in': 'body', 'required': True, 'schema': {'$ref': '#/definitions/Login'}}

**Tags:** auth

에러 코드
- 400 Bad Request: 잘못된 요청, 유효성 검사 실패, 잘못된 회원 ID 또는 PIN 번호.
- 401 Unauthorized: 잘못된 자격 증명 (회원 ID 나 PIN 번호가 잘못됨)
- 500 Internal Server Error: 서버에서 예기치 않은 오류 발생
  
### API: /auth/refresh
#### **Method:** POST
#### **Description:** 유효한 리프레시 토큰인 경우, 리프레시 타입 JSON 웹 토큰을 받아서 액세스 타입 JSON 웹 토큰을 반환합니다.
#### **OperationId:** auth_refresh_create
#### **Parameters:**
• - {'name': 'data', 'in': 'body', 'required': True, 'schema': {'$ref': '#/definitions/TokenRefresh'}}

**Tags:** auth

에러 코드
- 400 Bad Request: 잘못된 요청, refresh token 이 누락되거나 형식이 잘못된 경우.
- 401 Unauthorized: 만료된 refresh token, 유효하지 않은 refresh token.
- 500 Internal Server Error: 서버에서 예기치 않은 오류 발생

### API: /foodWaste/food-waste/
#### **Method:** GET
#### **Description:** 특정 사용자의 모든 음식물 쓰레기 기록을 조회합니다.
#### **OperationId:** foodWaste_food-waste_list
#### **Parameters:**• - {'name': 'user_id', 'in': 'query', 'description': 'User ID to filter food waste records', 
'type': 'string'}

**Tags:** foodWaste

에러 코드
- 400 Bad Request 잘못된 요청: 필수 파라미터가 누락되었을 때 발생
- 404 Not Found 사용자 없음: 제공된 user_id 로 사용자가 존재하지 않을 때 발생
- 500 Internal Server Error 서버 오류: 예기치 않은 오류 발생 시
  
### API: /foodWaste/food-waste/
#### **Method:** POST
#### **Description:** action_type 에 따라 음식물 쓰레기 기록을 추가하거나 감소시킵니다.
#### **OperationId:** foodWaste_food-waste_create
#### **Parameters:**
• - {'name': 'data', 'in': 'body', 'required': True, 'schema': {'required': ['user_id', 'quantity', 
'action_type'], 'type': 'object', 'properties': {'user_id': {'description': 'User ID', 'type': 
'string'}, 'quantity': {'description': 'Quantity index (0 to 5)', 'type': 'integer'}, 
'action_type': {'description': 'Action type: 0 for add, 1 for reduce', 'type': 'integer'}}}}

**Tags:** foodWaste

에러 코드
- 400 Bad Request: 요청 본문이 잘못되었거나 필수 필드인 user_id, quantity, action_type 가 누락된 경우 발생합니다.
- 400 Bad Request: action_type 값이 0 또는 1 외의 값이 들어간 경우 발생합니다.
- 400 Bad Request: quantity 값이 FoodWaste.QUANTITY_CHOICES 에 포함되지 않은 값일 경우 발생합니다.
- 500 Internal Server Error 서버 오류: 서버 내부 오류로 인해 음식물 쓰레기 기록을 처리할 수 없는 경우 발생합니다.

### API: /foodWaste/food-waste/delete-all/
#### **Method:** DELETE**Description:** 특정 사용자의 모든 음식물 쓰레기 기록을 삭제합니다.
#### **OperationId:** foodWaste_food-waste_delete_all
#### **Parameters:**
• - {'name': 'user_id', 'in': 'query', 'description': 'User ID to filter food waste records', 
'type': 'string'}

**Tags:** foodWaste

에러 코드
- 400 Bad Request: user_id 파라미터가 누락된 경우 발생합니다.
- 500 Internal Server Error 서버 오류: 서버 오류로 인해 음식물 쓰레기 기록을 삭제할 수
없는 경우 발생합니다.

### API: /foodWaste/food-waste/stats/daily/
#### **Method:** GET
#### **Description:** 특정 사용자의 하루 음식물 쓰레기 통계를 조회합니다.
#### **OperationId:** foodWaste_food-waste_stats_get_daily_stats
#### **Parameters:**
• - {'name': 'user_id', 'in': 'query', 'description': 'User ID to filter food waste records', 
'type': 'string'}

**Tags:** foodWaste

에러 코드
- 400 Bad Request: user_id 파라미터가 누락된 경우 발생합니다.
- 500 Internal Server Error 서버 오류: 서버 내부 오류로 인해 음식물 쓰레기 통계를
조회할 수 없는 경우 발생합니다.

### API: /foodWaste/food-waste/stats/monthly/
#### **Method:** GET
#### **Description:** 특정 사용자의 월간 음식물 쓰레기 통계를 조회합니다.
#### **OperationId:** foodWaste_food-waste_stats_get_monthly_stats**Parameters:**
• - {'name': 'user_id', 'in': 'query', 'description': 'User ID to filter food waste records', 
'type': 'string'}

**Tags:** foodWaste

에러 코드
- 400 Bad Request: user_id 파라미터가 누락된 경우 발생합니다.
- 500 Internal Server Error 서버 오류: 서버 오류로 인해 월간 통계를 조회할 수 없는 경우
발생합니다.

### API: /foodWaste/food-waste/stats/weekly/
#### **Method:** GET
#### **Description:** 특정 사용자의 주간 음식물 쓰레기 통계를 조회합니다.
#### **OperationId:** foodWaste_food-waste_stats_get_weekly_stats
#### **Parameters:**
• - {'name': 'user_id', 'in': 'query', 'description': 'User ID to filter food waste records', 
'type': 'string'}

**Tags:** foodWaste

에러 코드
- 400 Bad Request: user_id 파라미터가 누락된 경우 발생합니다.
- 500 Internal Server Error 서버 오류: 서버 오류로 인해 주간 통계를 조회할 수 없는 경우
발생합니다.

### API: /production/products/
#### **Method:** GET
#### **Description:** 선택적 필터링 조건에 따라 제품을 조회하고 요약 데이터를 제공합니다.
#### **OperationId:** production_products_list
#### **Parameters:**
• - {'name': 'user_id', 'in': 'query', 'description': 'Filter products by user ID', 'required': 
True, 'type': 'string'}
• - {'name': 'name', 'in': 'query', 'description': 'Filter products by name', 'type': 'string'}• - {'name': 'category', 'in': 'query', 'description': 'Filter products by category', 'type': 
'integer'}
• - {'name': 'location', 'in': 'query', 'description': 'Filter products by location', 'type': 
'integer'}
• - {'name': 'filter_type', 'in': 'query', 'description': '1: Imminent products (7 days or less), 
2: Expired products', 'type': 'string'}

**Tags:** production

에러 코드
- 400 Bad Request: 필수 파라미터 user_id 가 없거나 잘못된 값이 전달된 경우
- 500 Internal Server Error: 서버에서 예기치 않은 오류가 발생한 경우
API: /production/products/
### **Method:** POST
#### **Description:** 이미지 없이 소비기한을 직접 입력하여 제품을 생성합니다.
#### **OperationId:** production_products_create
#### **Parameters:**
• - {'name': 'name', 'in': 'formData', 'required': True, 'type': 'string', 'maxLength': 255, 
'minLength': 1}
• - {'name': 'expiration_date', 'in': 'formData', 'required': False, 'type': 'string', 'format': 
'date'}
• - {'name': 'category', 'in': 'formData', 'description': '0 : 미분류, 1 : 고기, 2 : 해산물, 3 : 
유제품, 4 : 야채, 5 : 음료, 6 : 과일, 7 : 기타', 'required': False, 'type': 'integer', 'enum': [0, 
1, 2, 3, 4, 5, 6, 7]}
• - {'name': 'location', 'in': 'formData', 'description': '0 : 냉장, 1 : 냉동, 2 : 상온, 3 : 미분류', 
'required': False, 'type': 'integer', 'enum': [0, 1, 2, 3]}
• - {'name': 'quantity', 'in': 'formData', 'required': False, 'type': 'integer', 'maximum': 
2147483647, 'minimum': -2147483648}
• - {'name': 'memo', 'in': 'formData', 'required': False, 'type': 'string', 'x-nullable': True}
• - {'name': 'image', 'in': 'formData', 'required': False, 'type': 'file', 'x-nullable': True}
• - {'name': 'user_id', 'in': 'formData', 'required': True, 'type': 'string', 'minLength': 1}

**Tags:** production

에러 코드
- 400 Bad Request: 필수 파라미터(user_id, name, expiration_date)가 없거나 잘못된 값이 전달된 경우.
- 500 Internal Server Error: 서버 내부 오류로 상품 생성에 실패한 경우

### API: /production/products/extract-expiration-date/
#### **Method:** POST
#### **Description:** 업로드된 이미지 파일에서 유통기한을 추출합니다.
#### **OperationId:** production_products_extract_expiration_date
#### **Parameters:**
• - {'name': 'image', 'in': 'formData', 'required': True, 'type': 'file'}

**Tags:** production

에러 코드
- 400 Bad Request: 유효하지 않은 이미지 파일이 전송된 경우, image 필드가 비어 있을 경우.
- 500 Internal Server Error: Vision API 요청 처리 오류, 자격 증명 또는 클라이언트 생성
오류.

### API: /production/products/{product_id}/
#### **Method:** PUT
#### **Description:** user_id 를 사용하여 특정 product_id 의 제품 정보를 업데이트합니다.
#### **OperationId:** production_products_update
#### **Parameters:**
• - {'name': 'name', 'in': 'formData', 'required': True, 'type': 'string', 'maxLength': 255, 
'minLength': 1}
• - {'name': 'expiration_date', 'in': 'formData', 'required': False, 'type': 'string', 'format': 
'date'}
• - {'name': 'category', 'in': 'formData', 'description': '0 : 미분류, 1 : 고기, 2 : 해산물, 3 : 
유제품, 4 : 야채, 5 : 음료, 6 : 과일, 7 : 기타', 'required': False, 'type': 'integer', 'enum': [0, 
1, 2, 3, 4, 5, 6, 7]}• - {'name': 'location', 'in': 'formData', 'description': '0 : 냉장, 1 : 냉동, 2 : 상온, 3 : 미분류', 
'required': False, 'type': 'integer', 'enum': [0, 1, 2, 3]}
• - {'name': 'quantity', 'in': 'formData', 'required': False, 'type': 'integer', 'maximum': 
2147483647, 'minimum': -2147483648}
• - {'name': 'memo', 'in': 'formData', 'required': False, 'type': 'string', 'x-nullable': True}
• - {'name': 'image', 'in': 'formData', 'required': False, 'type': 'file', 'x-nullable': True}
• - {'name': 'user_id', 'in': 'formData', 'required': True, 'type': 'string', 'minLength': 1}

**Tags:** production

에러 코드
- 400 Bad Request: user_id 파라미터가 요청 데이터에 포함되지 않은 경우, 필수 파라미터가 없거나 잘못된 값이 전달된 경우.
- 404 Not Found: 요청한 product_id 에 해당하는 상품이 존재하지 않는 경우
- 500 Internal Server Error: 서버 내부 오류로 상품 업데이트에 실패한 경우.

API: /production/products/{product_id}/
**Method:** DELETE
**Description:** user_id 를 사용하여 특정 product_id 의 제품을 삭제합니다.
**OperationId:** production_products_delete
**Parameters:**
• - {'name': 'user_id', 'in': 'query', 'description': 'Filter products by user ID', 'required': 
True, 'type': 'string'}

**Tags:** production

에러 코드
- 400 Bad Request: user_id 파라미터가 요청에 포함되지 않은 경우.
- 404 Not Found: 요청한 product_id 에 해당하는 상품이 존재하지 않거나, user_id 가 일치하지 않는 경우.
- 403 Forbidden: 요청한 상품이 user_id 와 일치하지 않는 경우.

### API: /profile/profile
#### **Method:** POST**Description:** 사용자의 멤버(프로필)를 추가합니다.
#### **OperationId:** add_member
#### **Parameters:**
• - {'name': 'id', 'in': 'formData', 'required': True, 'type': 'integer'}
• - {'name': 'profile_image', 'in': 'formData', 'required': False, 'type': 'file'}
• - {'name': 'profile_name', 'in': 'formData', 'required': True, 'type': 'string', 'minLength': 1}
• - {'name': 'pin_num', 'in': 'formData', 'required': True, 'type': 'integer'}

**Tags:** Profile

에러 코드
- 400 Bad Request: 요청이 잘못되었을 경우, 예를 들어 필수 파라미터가 누락되었거나 잘못된 형식의 값이 전달된 경우.
- 400 Bad Request: 프로필 이미지 파일 형식이 잘못된 경우.
- 400 Bad Request: 프로필 이름(profile_name)이나 핀 번호(pin_num)가 필수 파라미터로 전달되지 않았을 경우.
- 500 Internal Server Error: 예기치 않은 서버 오류가 발생한 경우.

### API: /profile/profiles
#### **Method:** GET
#### **Description:** 사용자가 생성한 멤버(프로필) 목록을 조회합니다.
#### **OperationId:** get memberList
#### **Parameters:**
• - {'name': 'id', 'in': 'query', 'description': 'user id', 'required': True, 'type': 'integer'}

**Tags:** Profile

에러 코드
- 400 Bad Request: 필수 user_id 파라미터가 누락된 경우.
- 204 No Content: 해당 사용자에 대한 프로필이 존재하지 않을 경우.
- 500 Internal Server Error: 서버에서 예기치 않은 오류가 발생한 경우.

### API: /recipe/recipes
#### **Method:** GET
#### **Description:** 등록된 제품 데이터를 기반으로 추천 레시피를 조회합니다.
#### **OperationId:** get recipeList
#### **Parameters:**
• - {'name': 'prodNames', 'in': 'query', 'description': 'production-names', 'required': True, 
'type': 'array', 'items': {'type': 'string'}}

**Tags:** Recipe

에러 코드
- 400 Bad Request: prodNames 파라미터가 제대로 전달되지 않은 경우 발생합니다.
- 204 No Content: 요청된 재료 목록에 맞는 레시피가 없는 경우 발생합니다.
- 500 Internal Server Error: 서버에서 예기치 않은 오류가 발생한 경우 발생합니다.

### API: /user/check-verify-code
#### **Method:** POST
#### **Description:** 사용자가 입력한 인증번호를 확인합니다.
#### **OperationId:** checkVerifyCode
#### **Parameters:**
• - {'name': 'data', 'in': 'body', 'required': True, 'schema': {'required': ['code', 'email'], 
'type': 'object', 'properties': {'code': {'description': '인증번호', 'type': 'integer', 'format': 
'integer'}, 'email': {'description': '이메일 주소', 'type': 'string', 'format': 'email'}}}}

**Tags:** User

에러 코드
- 400 Bad Request: 요청 본문이 잘못되었거나 필수 필드인 email 이 누락된 경우 발생합니다.
- 500 Internal Server Error: 이메일 전송에 실패했거나 SMTP 관련 오류가 발생한 경우
발생합니다.

### API: /user/checkId
#### **Method:** GET
#### **Description:** 사용자의 아이디 중복 여부를 확인합니다.
#### **OperationId:** checkIdDuplication
#### **Parameters:**
• - {'name': 'id', 'in': 'query', 'description': 'id check', 'required': True, 'type': 'string'}
**Tags:** User
에러 코드:
- 400 Bad Request: 제공된 user_id 가 이미 존재하는 경우 발생합니다.
- 500 Internal Server Error: 서버에서 예기치 않은 문제가 발생한 경우 발생합니다.

### API: /user/send-verify-code
#### **Method:** POST
#### **Description:** 사용자의 이메일 주소로 인증 코드를 전송합니다.
#### **OperationId:** sendVerifyCode
#### **Parameters:**
• - {'name': 'data', 'in': 'body', 'required': True, 'schema': {'required': ['email'], 'type': 
'object', 'properties': {'email': {'description': '사용자의 이메일 주소', 'type': 'string', 
'format': 'email'}}}}

**Tags:** User

에러 코드
- 400 Bad Request: 제공된 인증 코드가 Redis 에 저장된 코드와 일치하지 않을 경우 발생합니다.
- 400 Bad Request: 제공된 이메일에 대한 인증 코드가 Redis 에 존재하지 않는 경우 발생합니다. (코드가 만료되었거나 처음부터 저장되지 않았을 수 있음)
- 500 Internal Server Error: 인증 코드 확인 과정에서 예기치 않은 오류가 발생한 경우.

### API: /user/signup
#### **Method:** POST
#### **Description:** 새로운 사용자를 등록합니다.
#### **OperationId:** register
#### **Parameters:**
• - {'name': 'data', 'in': 'body', 'required': True, 'schema': {'$ref': 
'#/definitions/CreateUser'}}

**Tags:** User

에러 코드
- 400 Bad Request: (잘못된 요청)
- 500 Internal Server Error: (서버 오류):

### API: /notice/notices
#### **Method:** POST
#### **Description:** 새로운 공지사항을 작성합니다.
#### **OperationId:** createNotice
#### **Parameters:**
• - {'name': 'data', 'in': 'body', 'required': True, 'schema': {'required': ['title', 'content'], 
'type': 'object', 'properties': {'title': {'description': '공지사항 제목', 'type': 'string'}, 
'content': {'description': '공지사항 내용', 'type': 'string'}}}}

**Tags:** Notice

에러 코드
- 400 Bad Request: 요청 본문이 잘못되었거나 필수 필드인 title 또는 content 가 누락된 경우 발생합니다.
- 500 Internal Server Error: 공지사항을 생성하는 중 서버 오류가 발생한 경우 발생합니다

### API: /notice/notices/ {notice_id}
#### **Method:** PUT
#### **Description:** 새로운 공지사항을 수정합니다.**OperationId:** updateNotice
#### **Parameters:**
• - {'name': 'data', 'in': 'body', 'required': True, 'schema': {'required': ['title', 'content'], 
'type': 'object', 'properties': {'title': {'description': '공지사항 제목', 'type': 'string'}, 
'content': {'description': '공지사항 내용', 'type': 'string'}}}}
• - {'name': 'notice_id', 'in': 'path', 'required': True, 'type': 'integer', 'description': '수정할
공지사항의 ID'}

**Tags:** Notice

에러 코드
- 400 Bad Request: 요청 본문이 잘못되었거나 필수 필드인 title 또는 content 가 누락된 경우 발생합니다.
- 404 Not Found: 제공된 notice_id 에 해당하는 공지사항을 찾을 수 없는 경우 발생합니다.
- 500 Internal Server Error: 공지사항을 생성하는 중 서버 오류가 발생한 경우 발생합니다

### API: /notice/notices/ {notice_id}
#### **Method:** DELETE
#### **Description:** 특정 공지사항을 삭제합니다.
#### **OperationId:** deleteNotice
#### **Parameters:**
- {'name': 'notice_id', 'in': 'path', 'required': True, 'type': 'integer', 'description': '삭제할
공지사항의 ID'}• - {'name': 'notice_id', 'in': 'path', 'required': True, 'type': 'integer', 
'description': '수정할 공지사항의 ID'}

**Tags:** Notice

에러 코드
- 404 Not Found: 제공된 notice_id 에 해당하는 공지사항을 찾을 수 없는 경우 발생합니다
- 500 Internal Server Error: 공지사항을 삭제하는 중 서버 오류가 발생한 경우 발생합니다

### [Swagger 사이트 바로가기](http://43.202.243.97/swagger/)

# Auth 패키지 문서 
### 'auth' 패키지는 사용자 인증을 처리하며, 로그인 기능 및 JWT 토큰 관리를 포함합니다. 아래는 패키지의 각 구성 요소에 대한 자세한 설명입니다.

#### serializers.py
`LoginSerializer`는 로그인 API 를 위한 입력 데이터를 검증하는 데 사용됩니다. 
`member_id`와 `pin_num`의 두 필드를 요구합니다.
class LoginSerializer(serializers.Serializer):
 member_id = serializers.IntegerField(required=True, write_only=True)
 pin_num = serializers.IntegerField(required=True, write_only=True)
#### service.py
`AuthService` 클래스는 인증에 대한 비즈니스 로직을 처리합니다. 사용자 자격 증명을
검증하고 핀 번호를 확인하며, JWT 토큰을 생성합니다.
class AuthService:
 @classmethod
 def login(cls, data, serializer_class):
 사용자 검증 및 JWT 토큰 생성 로직
#### views.py
`LoginAPIView`는 사용자 로그인을 위한 엔드포인트를 정의합니다. `AuthService` 클래스를
사용하여 비즈니스 로직을 처리하고, `LoginSerializer`를 통해 데이터 검증을 수행합니다.
class LoginAPIView(APIView):
 def post(self, request):
  AuthService 를 통한 사용자 로그인 처리
#### urls.py
`urls.py` 파일은 인증 관련 엔드포인트에 대한 경로를 정의합니다. `login`과 토큰 관리를
위한 `refresh`가 포함됩니다.
urlpatterns = [
 path('login', LoginAPIView.as_view(), name='login'), path('refresh', TokenRefreshView.as_view(), name='refresh'),
]

# User 패키지 문서
### 'user' 패키지는 사용자 관리를 담당하며, 회원가입, 아이디 중복 확인, 이메일 인증 및 인증코드 확인과 같은 기능을 제공합니다. 아래는 각 구성 요소에 대한 상세 설명입니다.

#### models.py
User 모델은 사용자 정보를 저장합니다. 주요 필드는 다음과 같습니다:
- id: 사용자 고유 ID (AutoField)
- user_id: 사용자 아이디 (CharField, unique)
- password: 사용자 비밀번호 (해싱 처리)
- email: 이메일 주소
- created_date: 생성일
- updated_date: 수정일
class User(models.Model):
 id = models.AutoField(primary_key=True)
 user_id = models.CharField(max_length=20, unique=True)
 password = models.CharField(max_length=100)
 email = models.CharField(max_length=30)
 created_date = models.DateTimeField(auto_now_add=True)
 updated_date = models.DateTimeField(auto_now=True)
#### serializers.py
`CreateUserSerializer`는 회원가입 요청 데이터를 검증하는 데 사용됩니다. 비밀번호 확인, 
아이디 중복 체크, 인증 확인 필드를 포함합니다.
class CreateUserSerializer(serializers.Serializer):
 user_id = serializers.CharField()
 password = serializers.CharField(write_only=True)
 password_check = serializers.CharField(write_only=True)
 email = serializers.CharField()
#### service.py
`UserService` 클래스는 회원가입, 아이디 중복 체크, 인증 코드 전송 및 확인 기능을 포함한
사용자 관련 비즈니스 로직을 처리합니다.
class UserService:
 def userSave(data, serializer_class):
 회원가입 로직 처리
views.py
`views.py` 파일에는 다음과 같은 API 엔드포인트가 정의되어 있습니다:
- `SignupAPIView`: 회원가입 처리
- `UserCheckAPIView`: 아이디 중복 확인
- `SendVerifyCode`: 이메일 인증 코드 전송
- `CheckVerifyCode`: 이메일 인증 코드 확인
#### urls.py
`urls.py` 파일은 사용자 관련 엔드포인트에 대한 경로를 정의합니다:
- /signup: 회원가입
- /checkId: 아이디 중복 확인
- /send-verify-code: 이메일 인증 코드 전송
- /check-verify-code: 이메일 인증 코드 확인
urlpatterns = [
 path('signup', SignupAPIView.as_view(), name='signup'),
 path('checkId', UserCheckAPIView.as_view(), name='checkId'),
 path('send-verify-code', SendVerifyCode.as_view(), name='sendVerifyCode'),
 path('check-verify-code', CheckVerifyCode.as_view(), name='checkVerifyCode')
]

# Profile 패키지 문서
### 'profile' 패키지는 사용자 멤버(프로필) 관리를 담당합니다. 주요 기능으로는 멤버 추가, 멤버 리스트 조회 등이 있으며, 각 기능은 API 로 제공됩니다.

#### models.pyProfile 모델은 사용자 멤버 정보를 저장합니다. 주요 필드는 다음과 같습니다:
- id: 프로필 고유 ID (AutoField)
- user: 사용자 정보와의 외래키 관계 (ForeignKey)
- profile_name: 프로필 이름 (CharField)
- pin_num: 핀 번호 (해싱 처리됨)
- leader_yn: 리더 여부 (BooleanField)
- created_date: 생성일
- updated_date: 수정일
class Profile(models.Model):
 id = models.AutoField(primary_key=True)
 user = models.ForeignKey(user.models.User, max_length=20, 
on_delete=models.PROTECT)
 profile_name = models.CharField(max_length=20)
 pin_num = models.CharField(max_length=128, null=False, blank=False)
 leader_yn = models.BooleanField(default=False)
 created_date = models.DateTimeField(auto_now_add=True)
 updated_date = models.DateTimeField(auto_now=True)
#### serializers.py
`CreateProfileSerializer`는 멤버 추가 요청 데이터를 검증하는 데 사용됩니다. PIN 번호의
유효성 및 입력 데이터의 유효성을 확인합니다.
class CreateProfileSerializer(serializers.Serializer):
 id = serializers.IntegerField(required=True, write_only=True)
 profile_name = serializers.CharField(required=True)
 pin_num = serializers.IntegerField(required=True, write_only=True)
#### service.py
`ProfileService` 클래스는 멤버 추가 및 멤버 리스트 조회와 관련된 비즈니스 로직을
처리합니다.
class ProfileService:
 def profileSave(data, serializer_class): # 멤버 추가 로직 처리
 def getProfileList(cls, userId):
 멤버 리스트 조회 로직
#### views.py
`views.py` 파일에는 다음과 같은 API 엔드포인트가 정의되어 있습니다:
- `MemberAPIView`: 멤버 추가 처리
- `MemberListAPIView`: 멤버 리스트 조회
class MemberAPIView(APIView):
 def post(self, request):
 ProfileService 를 통한 멤버 추가 처리
class MemberListAPIView(APIView):
 def get(self, request):
 ProfileService 를 통한 멤버 리스트 조회
#### urls.py
`urls.py` 파일은 프로필 관련 엔드포인트에 대한 경로를 정의합니다:
- /profile: 멤버 추가
- /profiles: 멤버 리스트 조회
urlpatterns = [
 path('profile', MemberAPIView.as_view(), name='profile'),
 path('profiles', MemberListAPIView.as_view(), name='profiles'),
]

# Production 패키지 문서
### 'production' 패키지는 사용자 제품 관리를 담당합니다. 주요 기능으로는 제품 등록, 조회, 수정, 삭제, 이미지에서 유통기한 추출 등이 있으며, 각 기능은 API 로 제공됩니다.

#### models.py
Product 모델은 제품 정보를 저장합니다. 주요 필드는 다음과 같습니다:
- product_id: 제품 고유 ID (UUIDField)- name: 제품 이름
- expiration_date: 소비기한
- category: 제품 카테고리
- location: 보관 장소
- quantity: 수량
- memo: 메모
- image: 제품 이미지
- user: 사용자 정보와의 외래키 관계
class Product(models.Model):
 product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, 
primary_key=True)
 name = models.CharField(max_length=255)
 expiration_date = models.DateField(default=date.today, null=False, blank=False)
 category = models.IntegerField(choices=[...], default=0)
 location = models.IntegerField(choices=[...], default=0)
 quantity = models.IntegerField(default=1)
 memo = models.TextField(blank=True, null=True)
 image = models.ImageField(upload_to='products/', blank=True, null=True)
 user = models.ForeignKey(user.models.User, on_delete=models.PROTECT)
#### serializers.py
`ProductCreateSerializer`는 제품 등록 요청 데이터를 검증하는 데 사용되며, 제품 생성 및
수정 시 활용됩니다. 또한, 소비기한 상태를 반환합니다.
class ProductCreateSerializer(serializers.ModelSerializer):
 user_id = serializers.CharField(write_only=True)
 product_id = serializers.UUIDField(read_only=True)
 expiration_status = serializers.SerializerMethodField()
#### service.py
`extract_and_parse_expiration_date` 함수는 이미지 파일에서 소비기한을 추출하고
파싱하는 로직을 제공합니다. Google Vision API 를 활용하여 텍스트를 감지합니다.
views.py`views.py` 파일에는 제품 관련 CRUD 및 유통기한 추출 API 가 정의되어 있습니다. 주요
클래스는 `ProductViewSet`으로, 다음과 같은 기능을 제공합니다:
- `list`: 제품 목록 조회 (필터링 지원)
- `create`: 제품 등록
- `update`: 제품 수정
- `destroy`: 제품 삭제
- `extract_expiration_date`: 이미지에서 유통기한 추출
#### urls.py
`urls.py` 파일은 제품 관련 엔드포인트에 대한 경로를 정의합니다:
- /products: 제품 CRUD API
- /products/extract-expiration-date: 이미지에서 유통기한 추출
urlpatterns = [
 path('', include(router.urls)),
]

# FoodWaste 패키지 문서
### 'food_waste' 패키지는 사용자 음식물 쓰레기 기록 관리를 담당합니다. 기능으로는 기록추가, 감소, 통계 데이터 조회(일별, 주별, 월별) 등이 있으며, 각 기능은 API 로 제공됩니다.

#### models.py
FoodWaste 모델은 음식물 쓰레기 데이터를 저장합니다. 주요 필드는 다음과 같습니다:
- quantity: 음식물 쓰레기 양 (1L, 2L, 3L, 5L, 10L, 20L)
- action_type: 추가(+) 또는 감소(-)
- date_recorded: 기록 생성 날짜
- date: 기록 대상 날짜
- user: 사용자 정보와의 외래키 관계
class FoodWaste(models.Model):
 quantity = models.IntegerField(choices=[...], default=0)
 action_type = models.IntegerField(choices=[...], default=0)
 date_recorded = models.DateField(auto_now_add=True) date = models.DateField(default=datetime.date.today)
 user = models.ForeignKey(user.models.User, on_delete=models.PROTECT)
#### serializers.py
`FoodWasteSerializer`는 음식물 쓰레기 데이터의 유효성을 검증하고, 기록 추가 및 조회 시
사용됩니다.
class FoodWasteSerializer(serializers.ModelSerializer):
 user_id = serializers.CharField(write_only=True)
 quantity = serializers.ChoiceField(choices=FoodWaste.QUANTITY_CHOICES)
 action_type = serializers.ChoiceField(choices=FoodWaste.ACTION_TYPE_CHOICES)
#### serviceslayer.py
서비스 레이어는 음식물 쓰레기 통계 데이터를 처리하는 로직을 제공합니다. 주요 함수:
- `get_daily_statistics`: 일별 통계 데이터 반환
- `get_weekly_statistics`: 주별 통계 데이터 반환
- `get_monthly_statistics`: 월별 통계 데이터 반환
- `reduce_food_waste`: 음식물 쓰레기 기록에서 지정된 양을 감소
#### views.py
`FoodWasteViewSet`은 음식물 쓰레기 관련 CRUD 및 통계 데이터를 처리하는 API 를
제공합니다. 주요 엔드포인트:
- `create`: 음식물 쓰레기 추가 또는 감소
- `list`: 특정 사용자의 모든 기록 조회
- `get_daily_stats`: 일별 통계 데이터 반환
- `get_weekly_stats`: 주별 통계 데이터 반환
- `get_monthly_stats`: 월별 통계 데이터 반환
- `delete_all`: 특정 사용자의 모든 기록 삭제
#### urls.py
`urls.py` 파일은 음식물 쓰레기 관련 엔드포인트에 대한 경로를 정의합니다:
- /food-waste: 음식물 쓰레기 CRUD API
- /food-waste/stats/daily: 일별 통계 데이터- /food-waste/stats/weekly: 주별 통계 데이터
- /food-waste/stats/monthly: 월별 통계 데이터
- /food-waste/delete-all: 모든 기록 삭제
urlpatterns = [
 path('', include(router.urls)),
]

# Recipe 패키지 문서
### Recipe 패키지는 사용자가 제공한 재료 목록을 기반으로 추천 레시피를 검색하는 기능을 제공합니다. 이 패키지는 레시피 모델, 서비스 계층, API 뷰 및 URL 구성 요소로 구성되어있으며, 효율적인 데이터 검색 및 처리를 지원합니다.

#### models.py
Recipe 모델은 레시피 데이터베이스 테이블과 매핑됩니다. 다음은 Recipe 모델의
정의입니다:
class Recipe(models.Model):
 id = models.AutoField(primary_key=True)
 food_name = models.CharField(max_length=100)
 material_name = models.TextField()
 class Meta:
 db_table = 'recipe'
 
#### serviceslayer.py
서비스 계층은 비즈니스 로직을 처리하며, 레시피 데이터 검색 및 필터링을 담당합니다.
class RecipeService:
 @classmethod
 def recipeList(cls, prod_names_list):
 try:
 recipeList = Recipe.objects.all()
 recipe_details = []
 for recipe in recipeList: food_name = str(recipe.food_name or "").lower()
 material_name = str(recipe.material_name or "")
 if material_name and all(word.lower() in material_name for word in 
prod_names_list):
 recipe_details.append({
 "recipeName": food_name,
 "ingredients": [ingredient.strip() for ingredient in material_name.split(",")]
 })
 return random.sample(recipe_details, min(5, len(recipe_details))) if recipe_details 
else []
 except Exception as e:
 logger.error(f"Error retrieving recipes: {e}")
 raise
 
#### views.py
RecipeListAPIView 는 사용자가 제공한 재료를 기반으로 추천 레시피를 검색하는
엔드포인트를 제공합니다.
class RecipeListAPIView(APIView):
 permission_classes = [permissions.IsAuthenticated]
 
 @swagger_auto_schema(
 operation_id='get recipeList',
 operation_description='추천 레시 리스트 조회',
 tags=['Recipe'],
 manual_parameters=[
 openapi.Parameter(
 name='prodNames',
 in_=openapi.IN_QUERY,
 type=openapi.TYPE_ARRAY,
 items=openapi.Items(type=openapi.TYPE_STRING),
 description='production-names',
 required=True,
 ),
 ],
 responses={201: '레시피 조회 성공', 204: '레시피 데이터 없음', 400: '잘못된 요청', 500: 
'서버 오류'}
 )
 def get(self, request): prod_names = request.query_params.get('prodNames', "")
 prod_names_list = prod_names.split(',')
 try:
 response_data = RecipeService.recipeList(prod_names_list)
 return Response({"message": "추천 레시피 조회에 성공했습니다.", "data": 
response_data}) if response_data else Response({'message': '레시피 데이터 없음'}, 
status=204)
 except Exception as e:
 logger.error(f"레시피 조회 중 오류 발생: {e}")
 return Response({'message': '서버 오류가 발생했습니다.'}, status=500)
 
#### urls.py
RecipeListAPIView 에 접근하기 위한 URL 라우팅 정의입니다.
from django.urls import path
from recipe.views import RecipeListAPIView
app_name = 'recipe'
urlpatterns = [
 path('recipes', RecipeListAPIView.as_view(), name='recipes'),
]
 
# Notice 패키지 문서
### 'notice' 패키지는. 사용자가 공지사항을 관리하는 기능을 제공합니다. 기능으로는 공지사항 생성, 수정, 삭제 등이 있으며, 각 기능은 API로 제공됩니다.

#### models.py
Notice 모델은 공지사항의 데이터를 저장합니다. 주요 필드는 다음과 같습니다:
- title: 공지사항 제목 (CharField)
- content: 공지사항 내용 (TextField)
- create_at: 작성일 (DateTimeField)
class Notice(models.Model):
 title = models.CharField(max_length=200) 
 content = models.TextField()
 created_at = models.DateTimeField(auto_now_add=True)serializers.py
`NoticeSerializer`는 음식물 쓰레기 데이터의 유효성을 검증하고, 기록 추가 및 조회 시 사용
됩니다.
class NoticeSerializer(serializers.ModelSerializer):
 class Meta:
 model = Notice
 fields = ['id', 'title', 'content', 'created_at']
#### views.py
`NoticeViewSet`은 공지사항 관련 CRUD를 처리하는 API를 제공합니다. 주요 엔드포인트:
- `list`: 공지사항 모든 기록 조회
- `create`: 공지사항 등록
- `update`: 공지사항 수정
- `destroy`: 공지사항 삭제
#### urls.py
`urls.py` 파일은 공지사항 관련 엔드포인트에 대한 경로를 정의합니다:
- /notice: 공지사항 CRUD API
urlpatterns = [
 path('notices', views.NoticeListCreate.as_view(), name='notice_list_create'),
 path('notices/<int:pk>', views.NoticeDetail.as_view(), name='notice_detail'),
]

# Nginx derectory
- 목적: Nginx는 웹 서버로, 클라이언트의 요청을 Django 애플리케이션 서버로 전달하고, 정적 파일을 서빙하는 역할을 합니다.
주요 설정:
- 리버스 프록시 설정 (location /): 클라이언트의 요청을 Django 서버로 전달
- 정적 파일 서빙 (location static/): /static/ 경로로 요청된 정적 파일을 서빙.- 파일 업로드 제한: client_max_body_size를 128MB로 설정.

# Static derectory
Django REST Framework와 관련된 설정 및 문서화와 관련된 파일들을 포함합니다.
#### drf-yasg
- 목적: Django REST Framework의 Swagger 문서화를 자동으로 생성하는 패키지입니다.
- 유지보수 시 유의사항: API 변경 시 문서화가 자동으로 갱신되지만, 엔드포인트나 모델 변경 시 Swagger 문서를 다시 확인해야 합니다.
#### rest_framework
- 목적: Django REST Framework의 핵심적인 파일들이 위치한 폴더입니다. API 엔드포인트와 직렬화기 등이 포함됩니다.
- 유지보수 시 유의사항: 새로운 API 엔드포인트 추가나 모델 변경 시, 직렬화기(serializers.py)를 수정해야 합니다.

# .env file
- 목적: 프로젝트에서 사용하는 환경 변수를 정의하는 파일로, 민감한 정보를 관리합니다. 
#### 주요 환경 변수:
- GOOGLE_APPLICATION_CREDENTIALS: Google Cloud 인증 파일 경로.
- SECRET_KEY: Django의 보안 키.
- DB_NAME, DB_USER, DB_PASSWORD, DB_HOST: 데이터베이스 설정.
- EMAIL_HOST_USER, EMAIL_HOST_PASSWORD: 이메일 발송 관련 설정.

# Dockerfile
- 목적: Django 애플리케이션을 Docker 컨테이너에서 실행할 수 있도록 설정합니다
#### 주요 설정:
- Python 3.12.4 이미지 사용
- requirements.txt를 사용하여 의존성 설치.
- Gunicorn을 사용하여 Django 애플리케이션 실행.

# docker-compose.yml
- 목적: 여러 Docker 컨테이너를 정의하고 실행하기 위한 설정 파일입니다.
#### 주요 설정:
- web 서비스: Django 애플리케이션 실행.
- db 서비스: PostgreSQL 데이터베이스 설정.
- 포트 노출: 8000번 포트로 Django 애플리케이션을 접근 가능.
- 서비스 의존성: web 서비스는 db 서비스가 실행된 후 시작.

# requirements.txt
- 목적 프로젝트에서 사용하는 Python 패키지 의존성을 정의하는 파일입니다.
#### 주요 패키지:
- Django: 웹 애플리케이션 프레임워크.
- djangorestframework: REST API 개발을 위한 확장.
- gunicorn: WSGI 서버, Django 실행.
- google-cloud-vision: Google Cloud Vision API 연동.
- celery: 비동기 작업 큐 시스템.
- redis: Redis 서버 연동.
- PyJWT: JWT 인증 관련 패키지



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
