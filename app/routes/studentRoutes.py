from flask import Blueprint, flash, jsonify, request, render_template, session, redirect, url_for
#from app.controllers import classroomController
#import app.controllers.studentController as studentController
from app.helper import studentHelper
from app.models import answerModel, assessmentModel, classroomModel, enrollmentModel, question_assessmentModel, studentModel, user_assessmentModel

student_bp = Blueprint('student', __name__)

@student_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('student.login'))

@student_bp.route('/login', methods=['GET', 'POST'])
def login():
    #if request.method == 'get':
    if request.method == 'POST':
        email = request.form.get('email','')
        password = request.form.get('password','')
        data = studentModel.find_account(email)
        if not data:
            flash('account does not exists', 'error')
            return redirect(url_for('student.login'))
        elif password == data['password']:
            session['user'] = data
            print("successfully")
            return redirect(url_for('student.dashboard'))
        else:
            flash('incorrect password', 'error')
            return redirect(url_for('student.login'))
    return render_template('studentTemplate/student_login_page.html')

@student_bp.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '')
        data = studentModel.find_account(email)
        if data:
            flash("account already exists", 'error')
            return redirect(url_for('student.register'))
        data = studentModel.insert_student(request.form)
        session['user'] = data
        return redirect(url_for('student.dashboard'))
    return render_template('studentTemplate/student_register_page.html')

@student_bp.route('/dashboard', methods=['GET'])
def dashboard():
    check = studentHelper.studentAccountCheck()
    if check:
        return check
    classrooms = enrollmentModel.getClasses()
    return render_template('studentTemplate/student_show_classes_page.html', classrooms = classrooms)

@student_bp.route('/join', methods =['GET', 'POST'])
def join():
    if request.method == "POST":
        classRoom = classroomModel.searchClassroom(request.form.get('code', ''))
        if not classRoom:
            flash("classroom does not exists", 'error') 
            return redirect(url_for('student.dashboard'))
        
        exists = enrollmentModel.searchClass(classRoom['id'])
        if exists:
            flash("classroom already joined", 'error') 
            return redirect(url_for('student.dashboard'))
        
        enrollmentModel.addStudent(classRoom)
        return redirect(url_for('student.dashboard'))
    
    check = studentHelper.studentAccountCheck()
    if check:
        return check
    return render_template('classroomTemplate/join_classroom.html')

@student_bp.route('/assessment/<int:assessment_id>', methods=['GET'])
def viewAssessment(assessment_id):
    check = studentHelper.studentAccountCheck()
    if check:
        return check
    assessment = user_assessmentModel.viewAssessment(assessment_id)
    if not assessment:
        user_assessmentModel.insertAssessment(assessment_id)
        assessment = user_assessmentModel.viewAssessment(assessment_id)
    # print(assessment)
    is_finished = user_assessmentModel.isAssessementFinished(assessment_id)
    # print(is_finished)
    return render_template('studentTemplate/view_assessment.html', assessment = assessment, is_finished = is_finished)

@student_bp.route('/take-assessment/<int:aid>', methods=['GET', 'POST'])
def takeAssessment(aid):
    check = studentHelper.studentAccountCheck()
    if check:
        return check
    questions = question_assessmentModel.getQuestions(aid)
    assessment = assessmentModel.isAutomatic(aid)
    uaid = user_assessmentModel.getUaidByAid(aid)
    print(assessment)
    # print(uaid)
    if request.method == 'POST':
        output = [{"qid": k, "answer": v} for k, v in request.form.items()]
        # print(output)
        if not assessment['is_automatic']:
            # uaid = user_assessmentModel.getUaidByAid(aid)
            answerModel.insertAnswers(uaid, output)
            user_assessmentModel.updateAssessment(uaid)
        else:
            answerModel.insertAnswers(uaid, output)
            questions = question_assessmentModel.getQuestions(aid)
            count = 0
            # continue the grading logic here
            for index, question in enumerate(questions):
                if question['is_sensitive']:
                    if question['answer'].strip() == output[index]['answer'].strip():
                        count += 1
                else:
                    if question['answer'].lower().strip() == output[index]['answer'].lower().strip():
                        count += 1
            user_assessmentModel.updateAssessment(uaid, count)
        is_finished = user_assessmentModel.isAssessementFinished(aid)
        return redirect(url_for('student.viewAssessment', assessment_id=aid, is_finished=is_finished))
    
    # answers = answerModel.getAnswers(uaid)
    
    return render_template('studentTemplate/take_assessment.html', questions = questions, assessment = assessment)

@student_bp.route('/view-assessment/<int:aid>', methods=['GET'])
def viewAnswers(aid):
    check = studentHelper.studentAccountCheck()
    if check:
        return check
    uaid = user_assessmentModel.getUaidByAid(aid)
    ua_details = user_assessmentModel.getUserAssessment(uaid)
    answers = answerModel.getAnswers(uaid)
    return render_template('studentTemplate/view_answers.html', answers=answers, ua_details = ua_details)
    
