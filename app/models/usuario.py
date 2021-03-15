from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
  return Usuario.query.get(int(id))


class Usuario(UserMixin, db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  nome = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  senha_hash = db.Column(db.String(128))
  nacionalidade = db.Column(db.String(32), index=True)
  estoques = db.relationship('Estoque', backref='usuario', lazy='dynamic')

  def set_senha(self, senha):
    self.senha_hash = generate_password_hash(senha)
  
  def check_senha(self, senha):
    return check_password_hash(self.senha_hash, senha)

  def __repr__(self):
    return '<Usuario {}>'.format(self.nome, self.email)