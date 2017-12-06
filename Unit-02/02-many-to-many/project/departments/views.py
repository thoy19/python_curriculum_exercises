from flask import redirect, render_template, request, url_for, Blueprint
from project.models import Department
from project import db
from project.forms import NewDepartmentForm



departments_blueprint = Blueprint(
    'departments',
    __name__,
    template_folder='templates'
)

#  Routes for departments go below here

@departments_blueprint.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		new_department = Department(request.form['name'])
		db.session.add(new_department)
		db.session.commit()
		return redirect(url_for('departments.index'))
	return render_template('departments/index.html', departments=Department.query.all())

@departments_blueprint.route('/new')
def new():
	form = NewDepartmentForm()
	return render_template('departments/new.html', form=form)

@departments_blueprint.route('/<int:id>/edit')
def edit(id):
	department = Department.query.get(id)
	form = NewDepartmentForm()
	form.name.data = department.name
	return render_template('departments/edit.html', form=form, department=department)

@departments_blueprint.route('/<int:id>', methods=['GET','DELETE','PATCH'])
def show(id):
	department = Department.query.get(id)
	form = NewDepartmentForm()
	if request.method == b'PATCH':
		department = Department.query.get(id)
		department.name = request.form['name']
		db.session.add(department)
		db.session.commit()
		return redirect(url_for('departments.index'))
	if request.method == b'DELETE':
		department = Department.query.get(id)
		db.session.delete(department)
		db.session.commit()
		return redirect(url_for('departments.index'))
	return render_template('departments/show.html', form=form, department=department)