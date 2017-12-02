from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from forms import UserForm, MessageForm
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/users-app-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
modus = Modus(app)


class User(db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.Text)
	last_name = db.Column(db.Text)
	messages = db.relationship('Message', backref='user', lazy='dynamic', cascade='all,delete')

	def __init__(self, first_name, last_name):
		self.first_name = first_name
		self.last_name = last_name

class Message(db.Model):

	__tablename__ = 'messages'
# DDL
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
# DML
	def __init__(self, content, user_id):
		self.content = content
		self.user_id = user_id

@app.route('/')
def root():
	return redirect(url_for('index'))

@app.route('/users', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		form = UserForm(request.form)
		if form.validate():
			new_user = User(request.form['first_name'], request.form['last_name'])
			db.session.add(new_user)
			db.session.commit()
			return redirect(url_for('index'))
		else:
			return render_template('users/new.html', form=form)
	return render_template('users/index.html', users=User.query.all())

@app.route('/users/new')
def new():
	user_form = UserForm()
	return render_template('users/new.html', form=user_form)

@app.route('/users/<int:id>', methods=['GET','PATCH', 'DELETE'])
def show(id):
	found_user = User.query.get(id)
	if request.method == b'PATCH':
		found_user.first_name = request.form['first_name']
		found_user.last_name = request.form['last_name']
		db.session.add(found_user)
		db.session.commit()
		return redirect(url_for('index'))
	if request.method == b'DELETE':
		db.session.delete(found_user)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('users/show.html', user=found_user)

@app.route('/users/<int:id>/edit')
def edit(id):
	found_user = User.query.get(id)
	return render_template('users/edit.html', user=found_user)


# MESSAGES 

# SEE ALL MESSAGES
@app.route('/users/<int:user_id>/messages', methods=['GET', 'POST'])
def messages_index(user_id):
	#find a user
	if request.method == 'POST':
		new_message = Message(request.form['content'], user_id)
		db.session.add(new_message)
		db.session.commit()
		return redirect(url_for('messages_index', user_id=user_id))
	
	return render_template('messages/index.html', user=User.query.get(user_id))

# NEW MESSAGE
@app.route('/users/<int:user_id>/messages/new', methods=['GET','POST'])
def messages_new(user_id):
	return render_template('messages/new.html', user=User.query.get(user_id))

#EDIT MESSAGE FORM
@app.route('/users/<int:user_id>/messages/<int:id>/edit')
def messages_edit(user_id, id):
	found_message = Message.query.get(id)
	return render_template('messages/edit.html', message=found_message)

# EDIT MESSAGE
@app.route('/users/<int:user_id>/messages/<int:id>', methods=['GET','PATCH','DELETE'])
def messages_show(user_id, id):
	found_message = Message.query.get(id)
	if request.method == b'PATCH':
		found_message.content = request.form['content']
		db.session.add(found_message)
		db.session.commit()
		return redirect(url_for('messages_index', user_id=user_id))
	if request.method == b'DELETE':
		db.session.delete(found_message)
		db.session.commit()
		return redirect(url_for('messages_index', user_id=user_id))
	return render_template('messages/show.html', message=found_message)


if __name__ == '__main__':
    app.run(debug=True,port=3000)