from app import app
from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models.forms import UsuarioForm
from app.models.forms import LoginForm
from app.models.forms import EstoqueForm
from app.models.usuario import Usuario
from app.models.estoque import Estoque
from app import db

@app.route("/")
def index():
  usuarios = Usuario.query.all()
  return render_template("index.html", usuarios=usuarios, isLogged=current_user.is_authenticated)

@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for("estoque"))
  form = LoginForm()
  if form.validate_on_submit():
    u = Usuario.query.filter_by(email=form.email.data).first()
    if u is None or not u.check_senha(form.senha.data):
      flash("Nome de usuário e/ou senha inválidos")
      return redirect(url_for("login"))
    login_user(u, remember=form.lembrar.data)
    return redirect(url_for("estoque"))
  return render_template("login.html", title="Entrar", form=form)

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for("login"))

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
  if current_user.is_authenticated:
    return redirect(url_for("estoque"))
  form = UsuarioForm()
  if form.validate_on_submit():
    u = Usuario(nome=form.nome.data, email=form.email.data,
      nacionalidade=form.nacionalidade.data)
    u.set_senha(form.senha.data)
    db.session.add(u)
    db.session.commit()
    return redirect(url_for("estoque"))
  return render_template("cadastro.html", form=form, isLogged=current_user.is_authenticated)

@app.route("/estoque")
def estoque():
  estoques = Estoque.query.all()
  return render_template("estoque.html", estoques=estoques, isLogged=current_user.is_authenticated)

@app.route("/estoque/cadastro", methods=['GET', 'POST'])
@login_required
def estoque_cad():
  form = EstoqueForm()
  if form.validate_on_submit():
    e = Estoque(produto_nome=form.produto_nome.data, produto_dsc=form.produto_dsc.data,
      qtd_estoque=form.qtd_estoque.data, preco=form.preco.data)
    db.session.add(e)
    db.session.commit()
    return redirect(url_for("estoque"))
  return render_template("estoque_cad.html", form=form, isLogged=current_user.is_authenticated)