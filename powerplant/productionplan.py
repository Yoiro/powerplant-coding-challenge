import logging

from flask import Blueprint, request, current_app, jsonify, Response

from powerplant.network import Network


bp_productionplan = Blueprint("productionplan", __name__, url_prefix="/productionplan")

@bp_productionplan.route('', methods=["POST"])
@bp_productionplan.route('/', methods=["POST"])
def compute_production_plan():
    current_app.logger.info(f"production plan requested for network")
    current_app.logger.debug(f"request.json")
    if request.json is None or type(request.json) is not dict:
        current_app.logger.warning("Tried to run a simulation without a dict type")
        return jsonify(message="Please provide some data in JSON format"), 400
    if request.json == {}:
        current_app.logger.warning("Tried to run a simulation without any data")
        return jsonify(message="Please provide a non-empty JSON object"), 400
    try:
        network = Network.load_network_from_json(payload=request.json)
        network.compute_production_plan()
        response = network.create_response()
        current_app.logger.info(response)
        current_app.logger.debug(f"answered {response}")
        return jsonify(response), 200
    # This is terrible, don't do this at home
    except Exception as e:
        current_app.logger.error("Unhandled exception happened (more information below).")
        current_app.logger.error(e)
        return jsonify(message=f"Something went wrong"), 500
