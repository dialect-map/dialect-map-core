# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request
from models import PaperReference
from globals import service


bp = Blueprint("references", __name__)


@bp.route("/references/<reference_id>", methods=["GET"])
def get_reference(reference_id: str):
    """
    Gets a paper reference from the underlying database
    :param reference_id: ID of the paper reference to get
    :return: HTTP 200 response
    """

    record = service.paper_refs.get(reference_id)
    return make_response(jsonify(record), 200)


@bp.route("/references/source/<paper_id>/<paper_rev>", methods=["GET"])
def get_reference_by_source_paper(paper_id: str, paper_rev: int):
    """
    Gets a paper reference from the underlying database
    :param paper_id: ID of the source paper references
    :param paper_rev: revision of the source paper references
    :return: HTTP 200 response
    """

    record = service.paper_refs.get_by_source_paper(paper_id, paper_rev)
    return make_response(jsonify(record), 200)


@bp.route("/references/target/<paper_id>/<paper_rev>", methods=["GET"])
def get_reference_by_target_paper(paper_id: str, paper_rev: int):
    """
    Gets a paper reference from the underlying database
    :param paper_id: ID of the target paper references
    :param paper_rev: revision of the target paper references
    :return: HTTP 200 response
    """

    record = service.paper_refs.get_by_target_paper(paper_id, paper_rev)
    return make_response(jsonify(record), 200)


@bp.route("/references", methods=["POST"])
def create_reference():
    """
    Creates a paper reference with the provided JSON body
    :return: HTTP 201 response
    """

    ref = PaperReference(request.json)
    resp = service.paper_refs.create(ref)
    return make_response({"id": resp}, 201)


@bp.route("/references/<reference_id>", methods=["DELETE"])
def delete_reference(reference_id: str):
    """
    Deletes a paper reference from the underlying database
    :param reference_id: ID of the paper reference to delete
    :return: HTTP 200 response
    """

    service.paper_refs.delete(reference_id)
    return make_response(jsonify({}), 204)
