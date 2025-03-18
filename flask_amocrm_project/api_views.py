"""Модуль API проекта"""
from flasgger import Swagger, swag_from
from flask import request, jsonify

from .config import TEMPLATE_SWAGG
from .main import app
from .utils.api_requests import (
    get_contact,
    get_lead,
    get_full_leads_list,
    post_leads,
)

swagger = Swagger(app, template=TEMPLATE_SWAGG)


@app.route("/api/v1/leads/", methods=("GET", "POST"))
@swag_from("swagg/leads_get.yml", methods=("GET",))
@swag_from("swagg/leads_post.yml", methods=("POST",))
def get_leads_list_and_post_leads_route():
    """Маршрут для получения списка сделок и их создания."""
    if request.method == "GET":
        response_data, status_code = get_full_leads_list()
    if request.method == "POST":
        subm_stud_ids_crm = [
            (lead["submission_id"], lead["student_id"])
            for lead in request.json
        ]
        subm_stud_ids_amocrm = []

        leads_list, _ = get_full_leads_list()
        unique_leads = []

        for page in leads_list["response_list"]:
            for lead in page["_embedded"]["leads"]:
                if lead["custom_fields_values"]:
                    for custom_field in lead["custom_fields_values"]:
                        if custom_field["field_name"] == "Номер заявки":
                            subm_id_amocrm = custom_field["values"][0]["value"]
                            contact_id = lead["_embedded"]["contacts"][0]["id"]
                            contact, _ = get_contact(contact_id)
                            for cont_cust_field in contact[
                                "custom_fields_values"
                            ]:
                                if (
                                    cont_cust_field["field_name"]
                                    == "student_id"
                                ):
                                    stud_id_amocrm = cont_cust_field["values"][
                                        0
                                    ]["value"]
                                    subm_stud_ids_amocrm.append(
                                        (subm_id_amocrm, stud_id_amocrm)
                                    )
        for i in range(len(request.json)):
            if subm_stud_ids_crm[i] not in subm_stud_ids_amocrm:
                unique_leads.append(request.json[i])
        response_data, status_code = post_leads(unique_leads)
        if not unique_leads:
            response_data = {"message": "Duplicate lead(s)"}
    return jsonify(response_data), status_code


@app.route("/api/v1/lead/<int:id>", methods=("GET",))
@swag_from("swagg/lead_get.yml", methods=("GET",))
def get_lead_route(id: int):
    """Маршрут для получения сделки по ID."""
    response_data, status_code = get_lead(id)
    return jsonify(response_data), status_code
