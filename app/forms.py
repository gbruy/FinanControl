from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField , SelectField, DateField
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

class TransactionForm(FlaskForm):
    tipo = SelectField('Tipo', choices = [('Receita', 'Receita'), ('Despesa', 'Despesa')], validators =[DataRequired()] )
    categoria = StringField('Categoria', validators=[DataRequired()])
    valor = FloatField('Valor', validators=[DataRequired()])
    data = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Salvar')
    
