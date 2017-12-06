from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, widgets
from wtforms.validators import DataRequired
from project.models import Tag

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MessageForm(FlaskForm):
	content = StringField('Content', validators=[DataRequired()])
	tags = MultiCheckboxField('Tags', coerce=int)
	def set_choices(self):
		self.tags.choices = [(d.id, d.content) for d in Tag.query.all()]

class DeleteForm(FlaskForm):
	pass