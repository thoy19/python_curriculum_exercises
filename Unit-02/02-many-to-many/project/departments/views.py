from flask import redirect, render_template, request, url_for, Blueprint
from project.models import Department, Employee
from project import db


departments_blueprint = Blueprint(
    'departments',
    __name__,
    template_folder='templates'
)

#  Routes for employees go below here


#  Routes for employees go below here
@departments_blueprint.route('/', methods=['GET','POST'])
def index(user_id):
	employee = Employee.query.get(user_id)
	if request.method == 'POST':
		new_department = Department(request.form['name'])
		db.session.add(new_department)
		db.session.commit()
		return redirect(url_for('departments.index', user_id=employee.id))
	return render_template('departments/index.html', employee=employee, departments=Department.query.all())

@departments_blueprint.route('/new')
def new(user_id):
	employee = Employee.query.get(user_id)
	return render_template('departments/new.html', employee=employee)

@departments_blueprint.route('/<int:id>/edit')
def edit(user_id, id):
	employee = Employee.query.get(user_id)
	department = Department.query.get(id)
	return render_template('departments/edit.html', id=department.id, department=department, employee=employee.id)

@departments_blueprint.route('/<int:id>', methods=['GET','DELETE','PATCH'])
def show(user_id, id):
	found_department = Department.query.get(id)
	employee = Employee.query.get(user_id)
	if request.method == b'PATCH':
		department = Department.query.get(id)
		department.name = request.form['name']
		department.years_at_company = request.form['years_at_company']
		db.session.add(department)
		db.session.commit()
		return redirect(url_for('departments.index'), user_id=found_department.employee.id)
	if request.method == b'DELETE':
		department = Department.query.get(id)
		db.session.delete(department)
		db.session.commit()
		return redirect(url_for('departments.index'))
	return render_template('departments/show.html', employee=employee.id)