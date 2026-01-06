from flask import Blueprint, jsonify, render_template, request, session, redirect

from app.models import question_assessmentModel, questionModel


question_bp = Blueprint('question', __name__)

@question_bp.route('/create', methods=['POST'])
def add_question():
    data = request.get_json()
    user_id = session['user']['id']
    questionModel.createQuestion(data, user_id)
    return jsonify(success=True)

@question_bp.route('/delete/<int:question_id>', methods=['GET'])
def delete_question(question_id):
    questionModel.deleteQuestion(question_id)
    return redirect(request.referrer or '/')

@question_bp.route('/delete/<int:question_id>/<int:assessment_id>', methods=['GET'])
def delete_question_from_assessment(question_id, assessment_id):
    questionModel.deleteQuestion(question_id, assessment_id)
    return redirect(f'/assessment/view/{assessment_id}')

@question_bp.route('/edit/<int:questions_id>/<int:assessment_id>', methods=['GET', 'POST'])
def edit_question( questions_id, assessment_id):
    if request.method == 'POST':
        question = request.form.get('question_text', '')
        question_type = request.form.get('question_type', '')        
        explanation = request.form.get('explanation', '')
        case_sensitive = request.form.get('case_sensitive', '')
        options = request.form.getlist('choice')
        if question_type == 'mc':
            answerIndex = request.form.get('answer', '')
            answer = options[int(answerIndex)-1]
        else:
            answer = request.form.get('answer', '')
        data = {
            'question': question,
            'type': question_type,
            'answer': answer,
            'explanation': explanation,
            'is_sensitive': case_sensitive == 'sensitive',
            'options': options
        }
        questionModel.updateQuestion(questions_id, data)
        return redirect(f'/assessment/view/{assessment_id}')
    question = questionModel.viewQuestion(questions_id)
    return render_template('assessmentTemplate/edit.html', question=question , assessment_id=assessment_id)

@question_bp.route('/edit/<int:question_id>', methods=['GET', 'POST'])
def edit_question_no_assessment(question_id):
    if request.method == 'POST':
        question = request.form.get('question_text', '')
        question_type = request.form.get('question_type', '')        
        explanation = request.form.get('explanation', '')
        case_sensitive = request.form.get('case_sensitive', '')
        options = request.form.getlist('choice')
        if question_type == 'mc':
            answerIndex = request.form.get('answer', '')
            answer = options[int(answerIndex)-1]
        else:
            answer = request.form.get('answer', '')
        data = {
            'question': question,
            'type': question_type,
            'answer': answer,
            'explanation': explanation,
            'is_sensitive': case_sensitive == 'sensitive',
            'options': options
        }
        questionModel.updateQuestion(question_id, data)
        return redirect('/instructor/questions')
    question = questionModel.viewQuestion(question_id)
    return render_template('instructorTemplate/edit_question.html', question=question)

@question_bp.route('/add_from_bank', methods=['POST'])
def add_questions_from_bank():
    data = request.get_json()
    # print(data)
    question_ids = data.get('question_ids', [])
    assessment_id = data.get('assessment_id')
    question_assessmentModel.addQuestionsFromBank(question_ids, assessment_id)
    return jsonify(success=True)