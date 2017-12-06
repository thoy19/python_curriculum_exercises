from flask import redirect, render_template, request, url_for, flash, Blueprint
from project.users.forms import UserForm
from project.models import User
from project import db, bcrypt

from sqlalchemy.exc import IntegrityError


users_blueprint = Blueprint(
	'users',
	__name__,
	template_folder='templates'
	)

@users_blueprint.route('/signup', methods =["GET", "POST"])
def signup():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            new_user = User(form.data['first_name'], form.data['last_name'], form.data['username'], form.data['password'])
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            return render_template('users/signup.html', form=form)
        return redirect(url_for('users.login'))
    return render_template('users/signup.html', form=form)


@users_blueprint.route('/login', methods = ["GET", "POST"])
def login():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        found_user = User.query.filter_by(username = form.data['username']).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(found_user.password, form.data['password'])
            if authenticated_user:
                return redirect(url_for('users.welcome'))
    return render_template('users/login.html', form=form)

@users_blueprint.route('/welcome')
def welcome():
    return render_template('users/welcome.html')


# @users_blueprint.route('/', methods=['GET', 'POST'])
# def index():
# 	delete_form = DeleteForm()
# 	if request.method == 'POST':
# 		form = UserForm(request.form)
# 		if form.validate():
# 			new_user = User(request.form['first_name'], request.form['last_name'])
# 			db.session.add(new_user)
# 			db.session.commit()
# 			flash('User Created!')
# 			return redirect(url_for('users.index'))
# 		else:
# 			return render_template('users/new.html', form=form)
# 	return render_template('users/index.html', users=User.query.all(), delete_form=delete_form)

# @users_blueprint.route('/new')
# def new():
# 	user_form = UserForm()
# 	return render_template('users/new.html', form=user_form)

# @users_blueprint.route('/<int:id>', methods=['GET','PATCH', 'DELETE'])
# def show(id):
# 	found_user = User.query.get(id)
# 	if request.method == b'PATCH':
# 		form = UserForm(request.form)
# 		if form.validate():
# 			found_user.first_name = form.first_name.data
# 			found_user.last_name = form.last_name.data
# 			db.session.add(found_user)
# 			db.session.commit()
# 			flash('User Updated!')
# 			return redirect(url_for('users.index'))
# 		return render_template('users/edit.html', user=found_user, form=form)
# 	if request.method == b'DELETE':
# 		delete_form = DeleteForm(request.form)
# 		if delete_form.validate():
# 			db.session.delete(found_user)
# 			db.session.commit()
# 			flash('User Deleted!')
# 		return redirect(url_for('users.index'))
# 	return render_template('users/show.html', user=found_user)

# @users_blueprint.route('/<int:id>/edit')
# def edit(id):
# 	found_user = User.query.get(id)
# 	user_form = UserForm(obj=found_user)
# 	return render_template('users/edit.html', user=found_user, form=user_form)
