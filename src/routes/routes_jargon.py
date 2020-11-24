# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request
from models import Jargon
from models import JargonCategoryMetrics
from models import JargonPaperMetrics
from ..main import service


bp = Blueprint("jargons", __name__)


# ------------------- Jargon model ------------------- #


@bp.route("/jargons/<jargon_id>", methods=["GET"])
def get_jargon(jargon_id: str):
    """
    Gets a jargon from the underlying database
    :param jargon_id: ID of the jargon to get
    :return: HTTP 200 response
    """

    record = service.jargons.get(jargon_id)
    return make_response(jsonify(record), 200)


@bp.route("/jargons", methods=["POST"])
def create_jargon():
    """
    Creates a jargon with the provided JSON body
    :return: HTTP 201 response
    """

    jargon = Jargon(request.json)
    resp = service.jargons.create(jargon)
    return make_response({"id": resp}, 201)


@bp.route("/jargons/<jargon_id>", methods=["DELETE"])
def delete_jargon(jargon_id: str):
    """
    Deletes a jargon from the underlying database
    :param jargon_id: ID of the jargon to delete
    :return: HTTP 204 response
    """

    service.jargons.delete(jargon_id)
    return make_response(jsonify({}), 204)


# ----------- Jargon Category Metrics model ----------- #


@bp.route("/jargons/category/metrics/<metric_id>", methods=["GET"])
def get_cat_metrics(metric_id: str):
    """
    Gets a jargon cat. metric from the underlying database
    :param metric_id: ID of the metric to get
    :return: HTTP 200 response
    """

    record = service.jargon_cat_metrics.get(metric_id)
    return make_response(jsonify(record), 200)


@bp.route("/jargons/category/metrics/<jargon_id>", methods=["GET"])
@bp.route("/jargons/category/metrics/<jargon_id>/<category_id>", methods=["GET"])
def get_cat_metrics_by_jargon(jargon_id: str, category_id: str = None):
    """
    Gets a jargon cat. metric from the underlying database
    :param jargon_id: ID of the jargon to get metrics from
    :param category_id: ID of the category to filter metrics by (optional)
    :return: HTTP 200 response
    """

    record = service.jargon_cat_metrics.get_by_jargon(jargon_id, category_id)
    return make_response(jsonify(record), 200)


@bp.route("/jargons/category/metrics", methods=["POST"])
def create_cat_metrics():
    """
    Creates a jargon cat. metrics with the provided JSON body
    :return: HTTP 201 response
    """

    metric = JargonCategoryMetrics(request.json)
    resp = service.jargon_cat_metrics.create(metric)
    return make_response({"id": resp}, 201)


@bp.route("/jargons/category/metrics/<metric_id>", methods=["DELETE"])
def delete_cat_metrics(metric_id: str):
    """
    Deletes a jargon cat. metrics from the underlying database
    :param metric_id: ID of the metric to delete
    :return: HTTP 204 response
    """

    service.jargon_cat_metrics.delete(metric_id)
    return make_response(jsonify({}), 204)


# ----------- Jargon Paper Metrics model ----------- #


@bp.route("/jargons/paper/metrics/<metric_id>", methods=["GET"])
def get_paper_metrics(metric_id: str):
    """
    Gets a jargon paper metric from the underlying database
    :param metric_id: ID of the metric to get
    :return: HTTP 200 response
    """

    record = service.jargon_paper_metrics.get(metric_id)
    return make_response(jsonify(record), 200)


@bp.route("/jargons/paper/metrics/<jargon_id>", methods=["GET"])
@bp.route("/jargons/paper/metrics/<jargon_id>/<paper_id>", methods=["GET"])
@bp.route("/jargons/paper/metrics/<jargon_id>/<paper_id>/<paper_rev>", methods=["GET"])
def get_paper_metrics_by_jargon(jargon_id: str, paper_id: str = None, paper_rev: int = None):
    """
    Gets a jargon paper metric from the underlying database
    :param jargon_id: ID of the jargon to get metrics from
    :param paper_id: ID of the paper to filter metrics by (optional)
    :param paper_rev: revision of the paper to filter metrics by (optional)
    :return: HTTP 200 response
    """

    record = service.jargon_paper_metrics.get_by_jargon(jargon_id, paper_id, paper_rev)
    return make_response(jsonify(record), 200)


@bp.route("/jargons/paper/metrics", methods=["POST"])
def create_paper_metrics():
    """
    Creates a jargon paper metrics with the provided JSON body
    :return: HTTP 201 response
    """

    metric = JargonPaperMetrics(request.json)
    resp = service.jargon_paper_metrics.create(metric)
    return make_response({"id": resp}, 201)


@bp.route("/jargons/paper/metrics/<metric_id>", methods=["DELETE"])
def delete_paper_metrics(metric_id: str):
    """
    Deletes a jargon paper metrics from the underlying database
    :param metric_id: ID of the metric to delete
    :return: HTTP 204 response
    """

    service.jargon_paper_metrics.delete(metric_id)
    return make_response(jsonify({}), 204)
