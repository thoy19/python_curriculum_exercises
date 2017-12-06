from flask import render_template, Blueprint, redirect, request, url_for
from project.models import Employee, Department
from project import db
from project.forms import NewEmployeeForm

employees_blueprint = Blueprint(
    'employees',
    __name__,
    template_folder='templates'
)

#  Routes for employees go below here
@employees_blueprint.route('/', methods=['GET','POST'])
def index():
	form = NewEmployeeForm()
	form.set_choices()
	if request.method == 'POST':
		new_employee = Employee(request.form['name'], request.form['years_at_company'])
		for department in form.departments.data:
			new_employee.departments.append(Department.query.get(department))
		db.session.add(new_employee)
		db.session.commit()
		return redirect(url_for('employees.index'))
	return render_template('employees/index.html', employees=Employee.query.all(), form=form)

@employees_blueprint.route('/new')
def new():
	form = NewEmployeeForm()
	form.set_choices()
	return render_template('employees/new.html', form=form)

@employees_blueprint.route('/<int:id>/edit')
def edit(id):
	from IPython import embed; embed()
	employee = Employee.query.get(id)
	departments = [department.id for department in employee.departments]
	form = NewEmployeeForm(departments=departments)
	form.set_choices()
	return render_template('employees/edit.html', departments=departments, employee=employee, form=form)

@employees_blueprint.route('/<int:id>', methods=['GET','DELETE','PATCH'])
def show(id):
	employee = Employee.query.get(id)
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
	return render_template('employees/show.html', employee = employee)