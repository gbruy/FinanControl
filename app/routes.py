from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_user, logout_user, current_user, login_required 
from app.models import Usuario , Transacao, Categoria
from app.forms import RegisterForm, LoginForm , TransactionForm
from app import db
from datetime import datetime
from app.graficos import gerar_grafico_despesas_mensais, gerar_grafico_receitas_por_categoria


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
            return redirect(url_for('main.dashboard'))
        else:
            flash('E-mail ou senha invalidos', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Voce foi deslogado com sucesso', 'info')
    return redirect(url_for('main.login'))



@bp.route('/nova_transacao', methods = ['GET', 'POST'])
@login_required
def nova_transacao():
    form = TransactionForm()
    if form.validate_on_submit():
        # Obter o ID da categoria selecionada
        categoria_selecionada = form.categoria.data
        categoria_id = categoria_selecionada.id if categoria_selecionada else None

        #Criar a nova transação
        nova_transacao = Transacao(
            usuario_id = current_user.id,
            tipo = form.tipo.data,
            categoria = form.categoria.data,
            valor = form.valor.data,
            data = form.data.data
        )
        db.session.add(nova_transacao)
        db.session.commit()
        flash('Transação Adicionada com sucesso', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template ('nova_transacao.html', form=form)

@bp.route('/dashboard')
@login_required
def dashboard():
    # Obter transações do usuário logado
    transacoes = Transacao.query.filter_by(usuario_id=current_user.id).all()

    # Calcular saldo total, receitas e despesas
    saldo_total = sum(t.valor if t.tipo == 'Receita ' else -t.valor for t in transacoes)
    total_receitas = sum(t.valor for t in transacoes if t.tipo == 'Receita')
    total_despesas = sum(-t.valor for t in transacoes if t.tipo == 'Despesa')

    #Gerar Graficos
    grafico_despesas_mensais = gerar_grafico_despesas_mensais(current_user.id)
    grafico_receitas_por_categoria = gerar_grafico_receitas_por_categoria(current_user.id)
    
    return render_template(
        'dashboard.html',
        usuario=current_user,
        saldo_total=saldo_total,
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        transacoes=transacoes,grafico_despesas_mensais=grafico_despesas_mensais,
        grafico_receitas_por_categoria=grafico_receitas_por_categoria
    )

@bp.route('/criar_categoria', methods=['POST'])
@login_required
def criar_categoria():
    #obtem os dados enviados via AJAX
    data = request.get_json()
    nome_categoria = data.get('nome')

    if nome_categoria:
        nova_categoria = Categoria(nome=nome_categoria, usuario_id =current_user.id)
        db.session.add(nova_categoria)
        db.session.commit()

        return jsonify({'success': True, 'categoria_id': nova_categoria.id})
    else:
        return jsonify({'success': False, 'message': 'Nome da Categoria Invalido'}), 400
    
@bp.route('/editar_categoria/<int:categoria_id>', methods = ['POST'])
@login_required
def editar_categoria(categoria_id):
    #Obtem os dados via AJAX
    data = request.get_json()
    novo_nome = data.get('nome')

    if novo_nome:
        #busca a categoria pelo ID
        categoria = Categoria.query.filter_by(id=categoria_id, usuario_id = current_user.id).first()
        if categoria:
            categoria.nome = novo_nome
            db.session.commit()
            return jsonify({'success': True})
    return jsonify({'success' : False , 'message': 'Categoria não encontrada'}), 400

@bp.route('/excluir_categoria/<int:categoria_id>', methods = ['DELETE'])
@login_required
def excluir_categoria(categoria_id):
    categoria = Categoria.query.filter_by(id = categoria_id, usuario_id = current_user.id).first()
    if categoria:
        db.session.delete(categoria)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify ({'success': False, 'message': 'Categoria não encontrara'}), 400

def init_app(app):
    app.register_blueprint(bp)