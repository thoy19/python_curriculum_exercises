from flask import redirect, render_template, request, url_for, Blueprint
from project.models import Department

departments_blueprint = Blueprint(
    'departments',
    __name__,
    template_folder='templates'
)

#  Routes for employees go below here
