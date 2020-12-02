# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request
from globals import service
from models import Jargon
from urllib import parse


bp = Blueprint("jargons", __name__)


# ------------------- Jargon model ------------------- #


@bp.route("/jargon/<jargon_id>", methods=["GET"])
def get_jargon(jargon_id: str):
    """
    Gets a jargon from the underlying database
    :param jargon_id: ID of the jargon to get
    :return: HTTP 200 response
    """

    record = service.jargons.get(jargon_id)
    return make_response(jsonify(record), 200)


@bp.route("/jargon/string/<jargon_str>", methods=["GET"])
def get_jargon_by_string(jargon_str: str):
    """
    Gets a jargon from the underlying database
    :param jargon_str: jargon string representation
    :return: HTTP 200 / HTTP 404 responses
    """

    string = parse.unquote(jargon_str)
    string = string.lower()
    record = service.jargons.get_by_string(string)

    if record:
        return make_response(jsonify(record), 200)
    else:
        return make_response(jsonify(record), 404)


@bp.route("/jargon", methods=["POST"])
def create_jargon():
    """
    Creates a jargon with the provided JSON body
    :return: HTTP 201 response
    """

    jargon = Jargon(request.json)
    resp = service.jargons.create(jargon)
    return make_response({"id": resp}, 201)


@bp.route("/jargon/<jargon_id>", methods=["DELETE"])
def delete_jargon(jargon_id: str):
    """
    Deletes a jargon from the underlying database
    :param jargon_id: ID of the jargon to delete
    :return: HTTP 204 response
    """

    service.jargons.delete(jargon_id)
    return make_response(jsonify({}), 204)
