import logging

from flask import Blueprint, request, current_app, jsonify, Response

from powerplant.network import Network


bp_productionplan = Blueprint("productionplan", __name__, url_prefix="/productionplan")

@bp_productionplan.route('', methods=["POST"])
@bp_productionplan.route('/', methods=["POST"])
def compute_production_plan():
    if request.json is None or type(request.json) is not dict:
        return jsonify(message="Please provide some data in JSON format"), 400
    if request.json == {}:
        return jsonify(message="Please provide a non-empty JSON object"), 400
    try:
        network = Network.load_network_from_json(payload=request.json)
        network.compute_production_plan()
        response = network.create_response()
        current_app.logger.info(response)
        return jsonify(response), 200
    # This is terrible, don't do this at home
    except Exception as e:
        return jsonify(message=f"Something went wrong"), 500
