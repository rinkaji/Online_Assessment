from flask import Blueprint, request, session


question_bp = Blueprint('question', __name__)

@question_bp.route('/create', methods=['POST'])
def add_question():
    data = request.get_json()
    print(data)
    print(session['id'])