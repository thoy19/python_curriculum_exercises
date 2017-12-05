from flask import render_template, Blueprint, redirect, request, url_for
from project.models import Employee, Department
from project import db



employees_blueprint = Blueprint(
    'employees',
    __name__,
    template_folder='templates'
)

#  Routes for employees go below here
@employees_blueprint.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		new_employee = Employee(request.form['name'], request.form['years_at_company'])
		db.session.add(new_employee)
		db.session.commit()
		return redirect(url_for('employees.index'))
	return render_template('employees/index.html', employees=Employee.query.all())

@employees_blueprint.route('/new')
def new():
	return render_template('employees/new.html')

@employees_blueprint.route('/<int:id>/edit')
def edit(id):
	employee = Employee.query.get(id)
	return render_template('employees/edit.html', employee=employee)

@employees_blueprint.route('/<int:id>', methods=['GET','DELETE','PATCH'])
def show(id):
	if request.method == b'PATCH':
		employee = Employee.query.get(id)
		employee.name = request.form['name']
		employee.years_at_company = request.form['years_at_company']
		db.session.add(employee)
		db.session.commit()
		return redirect(url_for('employees.index'))
	if request.method == b'DELETE':
		employee = Employee.query.get(id)
		db.session.delete(employee)
		db.session.commit()
		return redirect(url_for('employees.index'))
	return render_template('employees/show.html')