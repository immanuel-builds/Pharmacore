from flask import Blueprint, jsonify, request
from app.core.models.substance import Substance
from app.core.services.interaction_service import InteractionService
from app.core.services.clinical_service import ClinicalService
from app.core.services.simulation_service import SimulationService
from app.core.services.graph_service import GraphService

core_bp = Blueprint('core', __name__, url_prefix='/core')

@core_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "module": "core-intelligence"})

@core_bp.route('/substance/<name>', methods=['GET'])
def get_substance(name):
    substance = Substance.query.filter_by(name=name).first()
    if not substance:
        return jsonify({"status": "error", "error": "Substance not found"}), 404

    return jsonify({
        "status": "success",
        "data": substance.to_dict(),
        "meta": {
            "confidence": substance.confidence,
            "sources": [substance.source] if substance.source else []
        },
        "error": None
    })

@core_bp.route('/interactions', methods=['POST'])
def analyze_interactions():
    data = request.get_json()
    substances = data.get('substances', [])
    if not substances:
        return jsonify({"status": "error", "error": "No substances provided"}), 400

    results = InteractionService.analyze_interactions(substances)

    # Calculate aggregate confidence
    confidence = 0.0
    sources = set()
    if results:
        confidence = sum(r['confidence'] for r in results) / len(results)
        for r in results:
            if r['source']:
                sources.add(r['source'])

    return jsonify({
        "status": "success",
        "data": results,
        "meta": {
            "confidence": round(confidence, 2),
            "sources": list(sources)
        },
        "error": None
    })

@core_bp.route('/clinical', methods=['POST'])
def analyze_clinical():
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    if not symptoms:
        return jsonify({"status": "error", "error": "No symptoms provided"}), 400

    results = ClinicalService.analyze_symptoms(symptoms)

    return jsonify({
        "status": "success",
        "data": results,
        "meta": {
            "confidence": 1.0, # Clinical mapping confidence is high for seed data
            "sources": ["manual_clinical"]
        },
        "error": None
    })

@core_bp.route('/simulation', methods=['POST'])
def run_simulation():
    data = request.get_json()
    substances = data.get('substances', [])
    if not substances:
        return jsonify({"status": "error", "error": "No substances provided"}), 400

    # Enrichment: get half-life from DB if not provided
    for sub in substances:
        if 'half_life' not in sub:
            db_sub = Substance.query.filter_by(name=sub['name']).first()
            if db_sub:
                sub['half_life'] = db_sub.half_life_hours

    results = SimulationService.run_simulation(substances)

    return jsonify({
        "status": "success",
        "data": results,
        "meta": {
            "model": "first-order-decay",
            "confidence": 0.8
        },
        "error": None
    })

@core_bp.route('/graph', methods=['POST'])
def get_graph():
    data = request.get_json()
    substances = data.get('substances', [])
    if not substances:
        return jsonify({"status": "error", "error": "No substances provided"}), 400

    results = GraphService.get_graph(substances)

    return jsonify({
        "status": "success",
        "data": results,
        "meta": {
            "confidence": 1.0,
            "sources": ["mechanism_database"]
        },
        "error": None
    })
