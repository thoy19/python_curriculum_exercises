from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/practice_users_messages'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
modus = Modus(app)
db = SQLAlchemy(app)


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

	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __init__(self, content, user_id):
		self.content = content
		self.user_id = user_id



# USERS ROUTES

@app.route('/')
def root():
	return redirect(url_for('index'))

@app.route('/users', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		new_user = User(request.form['first_name'], request.form['last_name'])
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('users/index.html', users=User.query.all())

@app.route('/users/new')
def new():
	return render_template('users/new.html')

@app.route('/users/<int:id>', methods=['GET','PATCH','DELETE'])
def show(id):
	return render_template('users/show.html', id=User.query.get(id))

@app.route('/users/<int:id>/edit')
def edit(id):
	pass



if __name__ == '__main__':
	app.run(debug=True)