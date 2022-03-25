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

#### Endpoints:
1. [POST] Авторизация пользователя
    ```bash
    [POST] https://metrograddiplomtodd.ru/api/referral/login-sms/
    ```
   * Request body:
   ```bash
    {
      "phone": 12345678910
    }
   ```
    Затем запуститься celery таска, которое имитирует задержку на сервере и отправку СМС
    
    СМС код приходит в ответе на запрос, БЕЗ ЗАДЕРЖКИ(в тестовых целях).
2. Подтверждение
<br>

## Local Docs
### API документация:
1. Swagger: http://127.0.0.1:8000/api/docs/
2. Redoc: http://127.0.0.1:8000/api/redoc/



