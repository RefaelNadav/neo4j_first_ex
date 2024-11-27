from flask import Blueprint, jsonify


scoring_bp = Blueprint('scoring', __name__, url_prefix='/scoring')

@scoring_bp.route('/calculate_risk_score', methods=['POST'])
def calculate_risk_score():
    return jsonify('Calculating risk scores'), 200

@scoring_bp.route('/blacklist_management', methods=['POST'])
def manage_blacklist():
    return jsonify('Managing blacklists'), 200

@scoring_bp.route('/cumulative_risk_metrics', methods=['GET'])
def cumulative_risk_metrics():
    return jsonify('Providing cumulative risk metrics'), 200



