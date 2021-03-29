from app import app
from flask import request, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from app.models.forms import UsuarioForm, LoginForm, EstoqueForm, DeleteForm, AvaliacaoForm
from app.models.usuario import Usuario
from app.models.estoque import Estoque
from app.models.avaliacao import Avaliacao
from app import db

@app.route("/")
def index():
  usuarios = Usuario.query.all()
  u = None
  nome_usuario = ""
  if current_user.is_authenticated:
    u = int(current_user.get_id())
    nome_usuario = Usuario.query.get(u).nome
  return render_template("index.html", usuarios=usuarios, usuario_atual=u, nome_usuario=nome_usuario, Logged=current_user.is_authenticated)

@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for("estoques"))
  form = LoginForm()
  if form.validate_on_submit():
    u = Usuario.query.filter_by(email=form.email.data).first()
    if u is None or not u.check_senha(form.senha.data):
      flash("Nome de usuário e/ou senha inválidos")
      return redirect(url_for("login"))
    login_user(u, remember=form.lembrar.data)
    return redirect(url_for("estoques"))
  return render_template("login.html", title="Entrar", form=form)

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for("login"))

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
  if current_user.is_authenticated:
    return redirect(url_for("estoques"))
  form = UsuarioForm()
  if form.validate_on_submit():
    u = Usuario(nome=form.nome.data, email=form.email.data,
      nacionalidade=form.nacionalidade.data)
    u.set_senha(form.senha.data)
    db.session.add(u)
    db.session.commit()
    login_user(u)
    return redirect(url_for("estoques"))
  return render_template("cadastro.html", form=form)

@app.route("/<id>/editar", methods=['GET', 'POST'])
@login_required
def usuario_editar(id):
  form = UsuarioForm()
  u = Usuario.query.get(id)
  if u is None:
    return abort(404)
  if form.validate_on_submit():
    nome_check = Usuario.query.filter_by(nome=form.nome.data).first()
    email_check = Usuario.query.filter_by(email=form.email.data).first()
    
    if nome_check is not None and not u.nome:
      flash ("Nome de usuário já existente!")
      return redirect(url_for('usuario_editar', id=id))
    elif email_check is not None and not u.email:
      flash ("E-mail já existente!")
      return redirect(url_for('usuario_editar', id=id))
    elif (nome_check is not None and not u.nome) and (email_check is not None and not u.email):
      flash ("Nome de usuário e e-mail já existentes!")
      return redirect(url_for('usuario_editar', id=id))

    u.nome = form.nome.data
    u.email = form.email.data
    u.set_senha(form.senha.data)
    u.nacionalidade = form.nacionalidade.data
    db.session.commit()
    return redirect(url_for("index"))
  return render_template("usuario_edicao.html", form=form, usuario=u, Logged=current_user.is_authenticated)

@app.route("/<id>/excluir", methods=['GET', 'POST'])
@login_required
def usuario_excluir(id):
  form = DeleteForm()
  u = Usuario.query.get(id)
  if u is None:
    return abort(404)
  if form.validate_on_submit():
    db.session.delete(u)
    db.session.commit()
    return redirect(url_for("index"))
  return render_template("usuario_exclusao.html", form=form, usuario=u, Logged=current_user.is_authenticated)

@app.route("/estoques")
def estoques():
  estoques = Estoque.query.all()
  u = None
  if current_user.is_authenticated:
    u = int(current_user.get_id())
  return render_template("estoques.html", estoques=estoques, usuario_atual=u, Logged=current_user.is_authenticated)

@app.route("/estoques/novo", methods=['GET', 'POST'])
@login_required
def estoque_novo():
  form = EstoqueForm()
  u = int(current_user.get_id())
  if u is None:
    return abort(404)
  if form.validate_on_submit():
    e = Estoque(produto_nome=form.produto_nome.data, produto_dsc=form.produto_dsc.data,
      qtd_estoque=form.qtd_estoque.data, preco=form.preco.data, usuario_id=u)
    db.session.add(e)
    db.session.commit()
    return redirect(url_for("estoques"))
  return render_template("estoque_novo.html", form=form, Logged=current_user.is_authenticated)

@app.route("/estoques/<id>/editar", methods=['GET', 'POST'])
@login_required
def estoque_editar(id):
  form = EstoqueForm()
  e = Estoque.query.get(id)
  if e is None:
    return abort(404)
  if form.validate_on_submit():
    pn_check = Estoque.query.filter_by(produto_nome=form.produto_nome.data).first()
    if pn_check is not None and not e.produto_nome:
      flash("Nome de produto já registrado!")
      return redirect(url_for('estoque_editar', id=id))
    e.produto_nome = form.produto_nome.data
    e.produto_dsc = form.produto_dsc.data
    e.qtd_estoque = form.qtd_estoque.data
    e.preco = form.preco.data
    db.session.commit()
    return redirect(url_for("estoques"))
  return render_template("estoque_edicao.html", form=form, estoque=e, Logged=current_user.is_authenticated)

@app.route("/estoques/<id>/excluir", methods=['GET', 'POST'])
@login_required
def estoque_excluir(id):
  form = DeleteForm()
  e = Estoque.query.get(id)
  if e is None:
    return abort(404)
  if form.validate_on_submit():
    db.session.delete(e)
    db.session.commit()
    return redirect(url_for("estoques"))
  return render_template("estoque_exclusao.html", form=form, estoque=e, Logged=current_user.is_authenticated)

@app.route("/estoques/<id_e>/avaliacoes")
def estoque_avaliacoes(id_e):
  avaliacoes = Avaliacao.query.filter_by(estoque_id=id_e)
  u = None
  if current_user.is_authenticated:
    u = int(current_user.get_id())
  return render_template("avaliacoes.html", avaliacoes=avaliacoes, usuario_atual=u, estoque_id=id_e, Logged=current_user.is_authenticated)

@app.route("/estoques/<id_e>/avaliar", methods=['GET', 'POST'])
@login_required
def estoque_avaliar(id_e):
  form = AvaliacaoForm()
  e = Estoque.query.get(id_e)
  id_u = int(current_user.get_id())
  u = Usuario.query.get(id_u)
  if e is None:
    return abort(404)
  if form.validate_on_submit():
    a = Avaliacao(autor=u.nome, nota=form.nota.data, comentario=form.comentario.data, usuario_id=id_u, estoque_id=id_e)
    db.session.add(a)
    db.session.commit()
    return redirect(url_for("estoque_avaliacoes", id_e=id_e))
  return render_template("estoque_avaliacao.html", form=form, estoque=e, Logged=current_user.is_authenticated)

@app.route("/estoques/<id_e>/avaliacoes/<id_a>/excluir", methods=['GET', 'POST'])
@login_required
def estoque_avaliacao_excluir(id_e, id_a):
  form = DeleteForm()
  a = Avaliacao.query.get(id_a)
  if a is None:
    return abort(404)
  db.session.delete(a)
  db.session.commit()
  return redirect(url_for("estoque_avaliacoes", id_e=id_e))



@app.errorhandler(404)
def not_found_error(error):
  return render_template("erro.html", cod_erro=404, desc_erro="Página não encontrada!"), 404

@app.errorhandler(500)
def internal_error(error):
  db.session.rollback()
  return render_template("erro.html", cod_erro=500, desc_erro="Erro interno do servidor!"), 500