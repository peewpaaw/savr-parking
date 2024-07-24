Docker:
- ```docker-compose up -d --build```

.env:
``` 
SECRET_KEY=
BTS_TOKEN=
REDIS_HOST=
```

Миграции.

Если нет alembic.ini:
- ```alembic init migrations```
- В ```alembic.ini``` адрес бд
- В ```env.py``` правки в ```from myapp import mymodel```

Новая миграция:
- ```alembic revision --autogenerate -m "comment"```
- ```alembic upgrade heads```