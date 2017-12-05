from flask import Flask, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
import os

app = Flask(__name__)
modus = Modus(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/many-many-example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# import a blueprint that we will create
from project.employees.views import employees_blueprint
from project.departments.views import departments_blueprint

# register our blueprints with the application
app.register_blueprint(employees_blueprint, url_prefix='/employees')
app.register_blueprint(departments_blueprint, url_prefix='/employees/<int:user_id>/departments')

@app.route('/')
def root():
    # return redirect(url_for('employees.index'))
    return redirect(url_for('employees.index'))