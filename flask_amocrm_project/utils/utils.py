import http
import json
import logging

import requests

from datetime import datetime

from ..config import STATUSES_LEADS, ID_VOR

logger = logging.getLogger("API")


def date_str_to_unix(date_str: str):
    """Преобразование строки в unixtime."""
    return int(datetime.strptime(date_str, "%Y-%m-%d").timestamp())


def create_list_leads(data_json: list[dict]):
    """Создание списка сделок для отправки в amoCRM."""
    leads = list()
    for lead_data in data_json:
        lead = dict(
            name=str(
                f'{lead_data.get("airtable_id")} '
                f'{lead_data.get("course_code")}'
            ),
            price=int(lead_data.get("price")),
            status_id=STATUSES_LEADS[lead_data.get("status")],
            pipeline_id=ID_VOR,
            created_at=date_str_to_unix(lead_data.get("date_received")),
            score=None,
            custom_fields_values=[
                dict(
                    field_id=877329,
                    field_name="Номер заявки",
                    field_code=None,
                    field_type="text",
                    values=[
                        dict(
                            value=str(lead_data.get("submission_id")),
                        ),
                    ],
                ),
                dict(
                    field_id=877323,
                    field_name="Оплачено",
                    field_code=None,
                    field_type="numeric",
                    values=[
                        dict(
                            value=int(lead_data.get("amount_paid")),
                        ),
                    ],
                ),
                dict(
                    field_id=877335,
                    field_name="Дата заявки",
                    field_code=None,
                    field_type="date",
                    values=[
                        dict(
                            value=date_str_to_unix(
                                lead_data.get("date_received")
                            ),
                        ),
                    ],
                ),
            ],
            _embedded=dict(
                contacts=[
                    dict(
                        first_name=lead_data.get("student_name"),
                        last_name=lead_data.get("student_surname"),
                        name=str(
                            f'{lead_data.get("student_name")} '
                            f'{lead_data.get("student_surname")}'
                        ),
                        custom_fields_values=[
                            dict(
                                field_code="PHONE",
                                values=[
                                    dict(
                                        enum_code="WORK",
                                        value=lead_data.get("student_phone"),
                                    ),
                                ],
                            ),
                            dict(
                                field_code="EMAIL",
                                values=[
                                    dict(
                                        enum_code="WORK",
                                        value=lead_data.get("student_email"),
                                    )
                                ],
                            ),
                            dict(
                                field_id=880093,
                                field_name="student_id",
                                field_code=None,
                                field_type="text",
                                values=[
                                    dict(
                                        value=str(lead_data.get("student_id")),
                                    ),
                                ],
                            ),
                        ],
                    )
                ]
            ),
        )
        leads.append(lead)
    return leads


def try_except_decorator(func):
    """
    Декоратор перехвата ошибок обращения по URLs к API сервисов заказчика.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP Error: {http_err}")
            return (
                {"error": "HTTP Error", "message": str(http_err)},
                http.HTTPStatus.BAD_REQUEST,
            )
        except json.JSONDecodeError as json_err:
            logger.error(f"JSON Decode Error: {json_err}")
            return (
                {"error": "JSON Decode Error", "message": str(json_err)},
                http.HTTPStatus.UNPROCESSABLE_ENTITY,
            )
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f"Connection Error: {conn_err}")
            return (
                {"error": "Connection Error", "message": str(conn_err)},
                http.HTTPStatus.BAD_GATEWAY,
            )
        except requests.exceptions.Timeout as timeout_err:
            logger.error(f"Timeout Error: {timeout_err}")
            return (
                {"error": "Timeout Error", "message": str(timeout_err)},
                http.HTTPStatus.GATEWAY_TIMEOUT,
            )
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Request Error: {req_err}")
            return (
                {"error": "Request Error", "message": str(req_err)},
                http.HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        except ValueError as val_err:
            return (
                dict(error=f"Invalid symbol: {val_err}"),
                http.HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    return wrapper
