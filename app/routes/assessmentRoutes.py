from flask import Blueprint, redirect, render_template, request, url_for

#from app.controllers import assessmentController
from app.helper.instructorHelper import accountCheck
from app.models import answerModel, assessmentModel, optionModel, questionModel, user_assessmentModel


assessment_bp = Blueprint('assessment', __name__)

@assessment_bp.route('/create/<int:classroom_id>', methods = ['GET', 'POST'])
def create(classroom_id):
    if request.method == "POST":
        assessmentModel.createAssessment(classroom_id, request.form)
        return redirect(url_for('classroom.view', id=classroom_id))
    check = accountCheck()
    if check:
        return check
    return render_template('assessmentTemplate/create.html', classroom_id = classroom_id)

@assessment_bp.route('/view/<int:assessment_id>', methods = ['GET'])
def view(assessment_id):
    check = accountCheck()
    if check:
        return check
    questions = questionModel.getQuestions(assessment_id)
    assessmentModel.updateQuestionCount(assessment_id, len(questions))
    assessment = assessmentModel.viewAssessment(assessment_id)
    questionsBank = questionModel.getAllQuestions()
    
    #if assessement is deployed, show student list
    if assessment.get('status') == 'deployed':
        students = user_assessmentModel.getStudentsWithAssessment(assessment_id)
        uaids = [student['uaid'] for student in students]
        # print(uaids)
        answers = answerModel.getAnswersByUaids(uaids)
        print(answers)
        return render_template('assessmentTemplate/view_student_assessment.html', assessment = assessment, questions = questions, students = students, answers = answers)
    
    existingQ = [q['id'] for q in questions]
    return render_template('assessmentTemplate/view.html', assessment = assessment, questions = questions, questionsBank = questionsBank, existingQ = existingQ)

@assessment_bp.route('/deploy/<int:assessment_id>', methods = ['GET'])
def deploy(assessment_id):
    check = accountCheck()
    if check:
        return check
    assessmentModel.deployAssessment(assessment_id)
    assessment = assessmentModel.viewAssessment(assessment_id)
    classroom_id = assessment.get('classroom_id')
    return redirect(url_for('classroom.view', id=classroom_id))

@assessment_bp.route('/check/<int:uaid>', methods = ['POST'])
def check(uaid):
    check = accountCheck()
    if check:
        return check
    data = request.get_json()
    # print(data)
    user_assessmentModel.updateUserAssessment(uaid, data)
    assessment = user_assessmentModel.getUserAssessment(uaid)
    answerModel.updateAnswers(data)
    return redirect(url_for('assessment.view', assessment_id = assessment['id']))