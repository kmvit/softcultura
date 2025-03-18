"""Модуль заросов API проекта."""

import http
import logging
import os

import requests

from dotenv import load_dotenv

from .utils import create_list_leads, try_except_decorator
from ..config import GET_CONTACT, GET_LEAD, GET_LEADS_LIST, POST_LEADS

logger = logging.getLogger("Flask_App")

load_dotenv()


@try_except_decorator
def get_full_leads_list():
    """Получение полного списка сделок."""
    response_list = []
    flag = True
    i = 1
    while flag:
        page = requests.get(
            GET_LEADS_LIST.format(i),
            headers={"Authorization": f"Bearer {os.getenv('TOKEN_AMO')}"},
            timeout=10,  # Устанавливаем тайм-аут в 10 секунд
        )
        if page.status_code != http.HTTPStatus.OK:
            logger.error(f"Response status code: {page.status_code}")
            return {"error": "Authorization Error"}, page.status_code
        logger.info(f"Response status code: {page.status_code}")
        response_list.append(page.json())
        flag = "next" in page.json()["_links"].keys()
        i += 1
    response = {"response_list": response_list}
    return response, page.status_code


@try_except_decorator
def get_lead(id: int):
    """Получение сделки по ID."""
    response = requests.get(
        GET_LEAD.format(id),
        headers={"Authorization": f"Bearer {os.getenv('TOKEN_AMO')}"},
        timeout=10,
    )
    if response.status_code != http.HTTPStatus.OK:
        logger.error(f"Response status code: {response.status_code}")
        return {"error": "Lead not found"}, response.status_code
    logger.info(f"Response status code: {response.status_code}")
    return response.json(), response.status_code


@try_except_decorator
def post_leads(data_json: list[dict]):
    """Создание сделок в amoCRM."""
    response = requests.post(
        POST_LEADS,
        headers={
            "Authorization": f"Bearer {os.getenv('TOKEN_AMO')}",
            "Content-Type": "application/json",
        },
        json=create_list_leads(data_json),
        timeout=10,
    )
    if response.status_code != http.HTTPStatus.OK:
        logger.error(f"Response status code: {response.status_code}")
        return {"error": "Request error"}, response.status_code
    logger.info(f"Response status code: {response.status_code}")
    return response.json(), response.status_code


@try_except_decorator
def get_contact(id: int):
    """Получение контакта по ID."""
    response = requests.get(
        GET_CONTACT.format(id),
        headers={"Authorization": f"Bearer {os.getenv('TOKEN_AMO')}"},
        timeout=10,
    )
    if response.status_code != http.HTTPStatus.OK:
        logger.error(f"Response status code: {response.status_code}")
        return {"error": "Contact not found"}, response.status_code
    logger.info(f"Response status code: {response.status_code}")
    return response.json(), response.status_code
