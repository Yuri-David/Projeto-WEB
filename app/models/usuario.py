from app import db


class Usuario(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  nome = db.Column(db.String(64), index=True)
  senha = db.Column(db.String(64), index=True)
  email = db.Column(db.String(64), index=True)
  nacionalidade = db.Column(db.String(32), index=True)
  estoques = db.relationship('Estoque', backref='usuario', lazy='dynamic')

  def __repr__(self):
    return '<Usuario {} ({})>'.format(self.nome, self.email)