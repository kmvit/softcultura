# Проект от Софт Культура — внешнее решение-интеграция в виде amoCRM для REST API Софт Культуры.

## Стек проекта:
Python, Flask, Docker

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/kmvit/softcultura
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас Windows (Git Bash)

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Запустить проект (переходим в директорию flask_amocrm_project):

```
flask run
```

В случае возникновения ошибки:

```
export FLASK_APP=main.py
flask run
```
Для запуска проекта в контейнере перейти в директорию с файлом **docker-compose.yml**, выполнить запуск:

```
docker compose up
```
Полезно будет выполнить команду `docker system prune -af`: она уберёт все лишние объекты, которые вы могли создать в докере за время тестирования, — неиспользуемые контейнеры, образы и сети.

## Примеры запросов:

> Подробнее можно ознакомится в документации amoCRM https://www.amocrm.ru/developers/content/crm_platform/leads-api

### Получение списка сделок (GET-запрос):

```
http://127.0.0.1:5000/api/v1/leads/
```

Пример ответа:
```json
[{
    "_page": 1,
    "_links": {
        "self": {
            "href": "https://softculture.amocrm.ru/api/v4/leads?page=1&limit=250"
        },
        "next": {
            "href": "https://softculture.amocrm.ru/api/v4/leads?page=2&limit=250"
        }
    },
    "_embedded": {
        "leads": [
            {
                "id": 3637385,
                "name": "Связаться по заявке RHN_72 от 23.05",
                "price": 0,
                "responsible_user_id": 10998074,
                "group_id": 0,
                "status_id": 142,
                "pipeline_id": 8117898,
                "loss_reason_id": null,
                "created_by": 10998074,
                "updated_by": 10998074,
                "created_at": 1716469616,
                "updated_at": 1716550733,
                "closed_at": 1716550733,
                "closest_task_at": null,
                "is_deleted": false,
                "custom_fields_values": null,
                "score": null,
                "account_id": 31727418,
                "labor_cost": null,
                "_links": {
                    "self": {
                        "href": "https://softculture.amocrm.ru/api/v4/leads/3637385?page=1&limit=250"
                    }
                },
                "_embedded": {
                    "tags": [],
                    "companies": []
                }
            },
            {
                "id": 4482869,
                "name": "whatcrm: Елизавета",
                "price": 0,
                "responsible_user_id": 10998074,
                "group_id": 0,
                "status_id": 142,
                "pipeline_id": 8117898,
                "loss_reason_id": null,
                "created_by": 0,
                "updated_by": 10998074,
                "created_at": 1717320286,
                "updated_at": 1718206044,
                "closed_at": 1718206044,
                "closest_task_at": null,
                "is_deleted": false,
                "custom_fields_values": null,
                "score": null,
                "account_id": 31727418,
                "labor_cost": null,
                "_links": {
                    "self": {
                        "href": "https://softculture.amocrm.ru/api/v4/leads/4482869?page=1&limit=250"
                    }
                },
                "_embedded": {
                    "tags": [],
                    "companies": []
                }
            },
        ]
    }
}]
```

### Получение сделки по ID (GET-запрос):

```
http://127.0.0.1:5000/api/v1/leads/3637385
```

Пример ответа:
```json
[{
    "id": 3637385,
    "name": "Связаться по заявке RHN_72 от 23.05",
    "price": 0,
    "responsible_user_id": 10998074,
    "group_id": 0,
    "status_id": 142,
    "pipeline_id": 8117898,
    "loss_reason_id": null,
    "created_by": 10998074,
    "updated_by": 10998074,
    "created_at": 1716469616,
    "updated_at": 1716550733,
    "closed_at": 1716550733,
    "closest_task_at": null,
    "is_deleted": false,
    "custom_fields_values": null,
    "score": null,
    "account_id": 31727418,
    "labor_cost": null,
    "_links": {
        "self": {
            "href": "https://softculture.amocrm.ru/api/v4/leads/3637385?page=1&limit=250"
        }
    },
    "_embedded": {
        "tags": [],
        "companies": []
    }
}]
```

### Создание списка сделок (POST-запрос):

```
http://127.0.0.1:5000/api/v1/leads/
```

Пример запроса:
```json
[
  {
    "airtable_id": "M13752",
    "amount_paid": 7000.0,
    "course_code": "ISB_7.7.07",
    "date_received": "2021-10-01",
    "price": 7000.0,
    "student_email": "uuu@gmail.com",
    "student_id": "A9299",
    "student_name": "Name1",
    "student_phone": "+770000000000",
    "student_surname": "Surname1",
    "submission_id": "P18814",
    "status": "Оплачена полностью"
  },
  {
    "airtable_id": "M13753",
    "amount_paid": 472.0,
    "course_code": "ISB_7.7.07",
    "date_received": "2021-10-01",
    "price": 472.0,
    "student_email": "nnn@yandex.ru",
    "student_id": "A9299",
    "student_name": "Name2",
    "student_phone": "+770000000001",
    "student_surname": "Surname2",
    "submission_id": "P18814",
    "status": "Оплачена полностью"
  }
]
```

Пример ответа:
```json
[
    {
        "company_id": null,
        "contact_id": 18049401,
        "id": 14847813,
        "merged": false,
        "request_id": [
            "1"
        ]
    }
]
```

## Pre-commit

Для минимизации трудностей во время разработки и поддержании высокого качества кода в разработке мы используем `pre-commit`. Данный фреймворк позволяет проверить код на соответствие `PEP8`, защитить ветки master и develop от непреднамеренного коммита, проверить корректность импортов и наличие trailing spaces.
`Pre-commit` конфигурируется с помощью специального файл `.pre-commit-config.yaml`. Для использования фреймворка его необходимо установить, выполнив команду из активированного виртуального окружения:

```bash
pip install pre-commit==3.6.0
```
или 

```bash
pip install -r requirements-dev.txt
```

Для принудительной проверки всех файлов можно выполнить команду:
```bash
pre-commit run --all-files
```

При первом запуске будут скачаны и установлены все необходимые хуки, указанные в конфигурационном файле.

Для автоматической проверки всех файлов необходимо инициализировать фреймворк командой:
```bash
pre-commit install
```