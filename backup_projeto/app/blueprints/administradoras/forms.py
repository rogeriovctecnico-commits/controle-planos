from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class AdministradoraForm(FlaskForm):
    nome_administradora = StringField('Nome da Administradora', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Salvar')