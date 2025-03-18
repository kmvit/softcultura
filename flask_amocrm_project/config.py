"""Модуль настроек и констант проекта"""

import os
from datetime import timedelta


# # Config Flask
class Config(object):
    """Конфиг фласк."""

    # Не переопределяем словарь, а сразу формируем с нужными значениями
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SECRET_KEY = os.getenv("SECRET_KEY", default="default")


# Отношение состояний сделки
STATUSES_LEADS = {
    "Нет оплаты": 66431750,
    "Оплачена полностью": 142,
    "Оплачена частично": 142,
    "Оплачена с переплатой": 142,
    "Отменена": 143,
}

# ID воронки "Воронка" в проекте amoCRM
ID_VOR = 8117898

# # Глобальные настройки логгера
BACKUP_COUNT = 5
ENCODING = "UTF-8"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
LOGGING_LEVEL = "DEBUG"
LOGS_FOLDER = "logs"
LOGS_FILE = "logfile.log"
MAX_BYTES = 50_000_000

# URL's amoCRM -- contacts
GET_CONTACT = "https://softculture.amocrm.ru/api/v4/contacts/{}"

# URL's amoCRM -- leads
BASE_URL = "https://softculture.amocrm.ru/api/v4/leads"
GET_LEADS_LIST = BASE_URL + "?with=contacts&page={}&limit=250"
GET_LEAD = BASE_URL + "/{}?with=contacts"
POST_LEADS = BASE_URL + "/complex"

# "swagger"
TEMPLATE_SWAGG = dict(
    swagger="2.0",
    info=dict(
        title="Проект интеграции API amoCRM.",
        description="Интеграция API заказчика, на API amoCRM.",
        version="0.0.1",
    ),
)
