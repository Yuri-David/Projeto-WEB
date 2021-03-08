from app import app
from flask import request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.forms import UsuarioForm
from app.models.forms import EstoqueForm
from app.models.usuario import Usuario
from app.models.estoque import Estoque
from app import db

@app.route("/")
def index():
  usuarios = Usuario.query.all()
  return render_template("index.html", usuarios=usuarios)

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
  form = UsuarioForm()
  if form.validate_on_submit():
    u = Usuario(nome=form.nome.data, email=form.email.data,
      senha=form.senha.data, nacionalidade=form.nacionalidade.data)
    db.session.add(u)
    db.session.commit()
    return redirect(url_for("index"))
  return render_template("cadastro.html", form=form)

@app.route("/estoque")
def estoque():
  estoques = Estoque.query.all()
  return render_template("estoque.html", estoques=estoques)

@app.route("/estoque/cadastro", methods=['GET', 'POST'])
def estoque_cad():
  form = EstoqueForm()
  if form.validate_on_submit():
    e = Estoque(produto_nome=form.produto_nome.data, produto_dsc=form.produto_dsc.data,
      qtd_estoque=form.qtd_estoque.data, preco=form.preco.data)
    db.session.add(e)
    db.session.commit()
    return redirect(url_for("estoque"))
  return render_template("estoque_cad.html", form=form)