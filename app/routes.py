from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required 
from app.models import Usuario
from app.forms import RegisterForm, LoginForm
from app import db


    # Cria um Blueprint para as rotas
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return 'Bem-vindo ao Finan Control'

def init_app(app):
    #Registra o Blueprint ao app
    app.register_blueprint(bp)

@bp.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        usuario = Usuario(nome = form.nome.data, email = form.email.data)
        usuario.set_senha(form.senha.data)
        db.session.add(usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)



@bp.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form=LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email = form.email.data).first()
        if usuario and usuario.verificar_senha(form.senha.data):
            login_user(usuario)
            flash('Login Realizado com Sucesso !' , 'success')
        else:
            flash('E-mail ou senha invalidos', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Voce foi deslogado com sucesso', 'info')
    return redirect(url_for('main.login'))

@bp.route('/dashboard')
@login_required  # Protege a rota para usuários logados
def dashboard():
    return render_template('dashboard.html', usuario=current_user)


def init_app(app):
    app.register_blueprint(bp)