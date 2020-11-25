# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request
from models import CategoryMembership
from globals import service


bp = Blueprint("memberships", __name__)


@bp.route("/membership/<membership_id>", methods=["GET"])
def get_membership(membership_id: str):
    """
    Gets a membership from the underlying database
    :param membership_id: ID of the membership to get
    :return: HTTP 200 response
    """

    record = service.category_memberships.get(membership_id)
    return make_response(jsonify(record), 200)


@bp.route("/membership", methods=["POST"])
def create_membership():
    """
    Creates a membership with the provided JSON body
    :return: HTTP 201 response
    """

    membership = CategoryMembership(request.json)
    resp = service.category_memberships.create(membership)
    return make_response({"id": resp}, 201)


@bp.route("/membership/<membership_id>", methods=["DELETE"])
def delete_membership(membership_id: str):
    """
    Deletes a membership from the underlying database
    :param membership_id: ID of the membership to delete
    :return: HTTP 200 response
    """

    service.category_memberships.delete(membership_id)
    return make_response(jsonify({}), 204)
