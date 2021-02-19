import logging

from flask import Blueprint, request, current_app, jsonify

from powerplant.network import Network


bp_productionplan = Blueprint("productionplan", __name__, url_prefix="/productionplan")

@bp_productionplan.route('', methods=["POST"])
@bp_productionplan.route('/', methods=["POST"])
def compute_production_plan():
    network = Network.load_network_from_json(payload=request.json)
    network.compute_production_plan()
    response = network.create_response()
    current_app.logger.info(response)
    return jsonify(network.create_response())
