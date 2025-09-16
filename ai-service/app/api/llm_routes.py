from flask import Blueprint, request, jsonify
from ..core.llm_service import generate_content

llm_bp = Blueprint('llm_bp', __name__)

@llm_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "O campo 'prompt' é obrigatório."}), 400

    try:
        response = generate_content(prompt)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
