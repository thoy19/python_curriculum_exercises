from flask import render_template, Blueprint, redirect
from project.models import Employee, Department



employees_blueprint = Blueprint(
    'employees',
    __name__,
    template_folder='templates'
)

#  Routes for employees go below here
@employees_blueprint.route('/', methods=['GET','POST'])
def index():
	return render_template('employees/index.html')
