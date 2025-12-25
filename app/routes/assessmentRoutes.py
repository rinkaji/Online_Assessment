from flask import Blueprint, redirect, render_template, request, url_for

#from app.controllers import assessmentController
from app.helper.instructorHelper import accountCheck
from app.models import assessmentModel


assessment_bp = Blueprint('assessment', __name__)

@assessment_bp.route('/create/<int:classroom_id>', methods = ['GET', 'POST'])
def create(classroom_id):
    if request.method == "POST":
        print(request.form)
        assessmentModel.createAssessment(classroom_id, request.form)
        return redirect(url_for('classroom.view', id=classroom_id))
    check = accountCheck()
    if check:
        return check
    return render_template('assessmentTemplate/create.html', classroom_id = classroom_id)