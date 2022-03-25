# Simple Referral System

Тестовое задание Hammer Systems - Простая реферальная система 

License: MIT

СТЕК:
1. Django/DjangoRestFramework
2. Postgres
3. Celery/Django Celery Beat
4. Redis
5. Docker
6. CI/CD


## Production Docs
### API документация:
1. Swagger: https://metrograddiplomtodd.ru/api/docs/
2. Redoc: https://metrograddiplomtodd.ru/api/redoc/

### Endpoints:
1. #### [POST] Авторизация пользователя
    ``` bash
    https://metrograddiplomtodd.ru/api/referral/login-sms/
    ```
   * Request body:
   ``` json
    {
      "phone": 213213
    }
   ```
   * Response:
   ``` json
    {
      "phone": "213213",
      "sms_code": 8164
    }
   ```
    Затем запуститься celery таска, которое имитирует задержку на сервере и отправку СМС
    
    СМС код приходит в ответе на запрос, БЕЗ ЗАДЕРЖКИ(в тестовых целях).


2. #### [POST] Подтверждение SMS кода
    ```bash
    https://metrograddiplomtodd.ru/api/referral/sms-code/
    ```
    * Request body:
    ```json
    {
      "code": 8164
    }
    ```
   * Response:
   ```json
    {
      "phone": "213213",
      "parent": null,
      "invite_code": "ucc5qe",
      "childs": [],
      "id": 2
    }
   ```


3. #### [GET] Профиль пользователя
    ```bash
   https://metrograddiplomtodd.ru/api/referral/profile/2/
    ```
   * Response:
   ```json
     {
      "phone": "213213",
      "parent": null,
      "invite_code": "ucc5qe",
      "childs": [],
      "id": 2
    }
   ```
   - `parent` - номер телефона пользователя, инвайт код которого активировал текущий пользователь
   - `childs` - номера телефонов пользователей, которые активировали инвайт код текущего пользователя
<br>

## Local Docs
### API документация:
1. Swagger: http://127.0.0.1:8000/api/docs/
2. Redoc: http://127.0.0.1:8000/api/redoc/



