# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request
from models import Paper
from models import PaperAuthor
from models import PaperReferenceCounters
from globals import service


bp = Blueprint("papers", __name__)


# ------------------- Paper model ------------------- #


@bp.route("/paper/<paper_id>/<paper_rev>", methods=["GET"])
def get_paper(paper_id: str, paper_rev: int):
    """
    Gets a paper from the underlying database
    :param paper_id: ID of the paper to get
    :param paper_rev: revision of the paper to get
    :return: HTTP 200 response
    """

    record = service.papers.get(paper_id, paper_rev)
    return make_response(jsonify(record), 200)


@bp.route("/paper", methods=["POST"])
def create_paper():
    """
    Creates a paper with the provided JSON body
    :return: HTTP 201 response
    """

    paper = Paper(request.json)
    resp = service.papers.create(paper)
    return make_response({"id": resp}, 201)


@bp.route("/paper/<paper_id>", methods=["DELETE"])
def delete_paper(paper_id: str):
    """
    Deletes a paper from the underlying database
    :param paper_id: ID of the paper to delete
    :return: HTTP 204 response
    """

    service.papers.delete(paper_id)
    return make_response(jsonify({}), 204)


@bp.route("/paper/<paper_id>/<paper_rev>", methods=["DELETE"])
def delete_paper_rev(paper_id: str, paper_rev: int):
    """
    Deletes a paper from the underlying database
    :param paper_id: ID of the paper to delete
    :param paper_rev: revision of the paper to delete
    :return: HTTP 204 response
    """

    service.papers.delete_rev(paper_id, paper_rev)
    return make_response(jsonify({}), 204)


# ---------------- Paper Author model ---------------- #


@bp.route("/paper/author/<author_id>", methods=["GET"])
def get_paper_author(author_id: str):
    """
    Gets a paper author from the underlying database
    :param author_id: ID of the paper author to get
    :return: HTTP 200 response
    """

    record = service.paper_authors.get(author_id)
    return make_response(jsonify(record), 200)


@bp.route("/paper/author/<paper_id>/<paper_rev>", methods=["GET"])
def get_paper_authors_by_paper(paper_id: str, paper_rev: int):
    """
    Gets a paper authors from the underlying database
    :param paper_id: ID of the paper to get the authors from
    :param paper_rev: revision of the paper to get the authors from
    :return: HTTP 200 response
    """

    record = service.paper_authors.get_by_paper(paper_id, paper_rev)
    return make_response(jsonify(record), 200)


@bp.route("/paper/author", methods=["POST"])
def create_paper_author():
    """
    Creates a paper author with the provided JSON body
    :return: HTTP 201 response
    """

    author = PaperAuthor(request.json)
    resp = service.paper_authors.create(author)
    return make_response({"id": resp}, 201)


@bp.route("/paper/author/<author_id>", methods=["DELETE"])
def delete_paper_author(author_id: str):
    """
    Deletes a paper author from the underlying database
    :param author_id: ID of the paper author to delete
    :return: HTTP 204 response
    """

    service.paper_authors.delete(author_id)
    return make_response(jsonify({}), 204)


# --------------- Paper Ref Counters model --------------- #


@bp.route("/paper/reference/counters/<counter_id>", methods=["GET"])
def get_ref_counter(counter_id: str):
    """
    Gets a paper ref. counter from the underlying database
    :param counter_id: ID of the paper ref. counter to get
    :return: HTTP 200 response
    """

    record = service.paper_ref_counters.get(counter_id)
    return make_response(jsonify(record), 200)


@bp.route("/paper/reference/counters/<paper_id>/<paper_rev>", methods=["GET"])
def get_ref_counter_by_paper(paper_id: str, paper_rev: int):
    """
    Gets a paper ref. counter from the underlying database
    :param paper_id: ID of the paper to get the ref. counter from
    :param paper_rev: revision of the paper to get the ref. counter from
    :return: HTTP 200 response
    """

    record = service.paper_ref_counters.get_by_paper(paper_id, paper_rev)
    return make_response(jsonify(record), 200)


@bp.route("/paper/reference/counters", methods=["POST"])
def create_ref_counter():
    """
    Creates a paper ref. counter with the provided JSON body
    :return: HTTP 201 response
    """

    counter = PaperReferenceCounters(request.json)
    resp = service.paper_ref_counters.create(counter)
    return make_response({"id": resp}, 201)


@bp.route("/paper/reference/counters/<counter_id>", methods=["DELETE"])
def delete_ref_counter(counter_id: str):
    """
    Deletes a paper ref. counter from the underlying database
    :param counter_id: ID of the paper ref. counter to delete
    :return: HTTP 204 response
    """

    service.paper_ref_counters.delete(counter_id)
    return make_response(jsonify({}), 204)
