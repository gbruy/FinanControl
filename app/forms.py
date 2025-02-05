from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    senha = StringField('Senha', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Cadastrar')

class LoginForm(FlaskForm):
    email = StringField('Email' ,validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')