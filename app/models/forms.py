from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class addMateria(FlaskForm): 
    pesquisa = StringField("pesquisa", validators=[DataRequired()])


