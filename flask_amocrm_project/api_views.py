"""Модуль API проекта"""
from flasgger import Swagger, swag_from
from flask import request, jsonify

from .config import TEMPLATE_SWAGG
from .main import app
from .utils.api_requests import get_lead, get_leads_list, post_leads

swagger = Swagger(app, template=TEMPLATE_SWAGG)


@app.route("/api/v1/leads/", methods=("GET", "POST"))
@swag_from("swagg/leads_get.yml", methods=("GET",))
@swag_from("swagg/leads_post.yml", methods=("POST",))
def get_leads_list_and_post_leads_route():
    """Маршрут для получения списка сделок и их создания."""
    if request.method == "GET":
        response_data, status_code = get_leads_list()
    if request.method == "POST":
        student_submission_ids_crm = [
            (lead["student_id"], lead["submission_id"])
            for lead in request.json
        ]
        leads_list, _ = get_leads_list()
        if leads_list:
            student_id_ids_amocrm = [
                (lead["student_id"], lead["id"])
                for lead in leads_list["_embedded"]["leads"]
            ]
        else:
            student_id_ids_amocrm = []
        unique_leads = []
        for i in range(len(request.json)):
            if student_submission_ids_crm[i] not in student_id_ids_amocrm:
                unique_leads.append(request.json[i])
            if not unique_leads:
                unique_leads = request.json
        response_data, status_code = post_leads(unique_leads)
    return jsonify(response_data), status_code


@app.route("/api/v1/lead/<int:id>", methods=("GET",))
@swag_from("swagg/lead_get.yml", methods=("GET",))
def get_lead_route(id: int):
    """Маршрут для получения сделки по ID."""
    response_data, status_code = get_lead(id)
    return jsonify(response_data), status_code
