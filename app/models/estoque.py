from app import db
from datetime import datetime


class Estoque(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  produto_nome = db.Column(db.String(64), index=True, unique=True)
  produto_dsc = db.Column(db.String(512), index=True)
  qtd_estoque = db.Column(db.Integer(), index=True)
  qtd_vendidos = db.Column(db.Integer(), index=True)
  preco = db.Column(db.Float(), index=True)
  timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
  usuario_id = db.Column(db.Integer(), db.ForeignKey('usuario.id'))
  avaliacoes = db.relationship('Avaliacao', backref='estoque', lazy='dynamic')

  def __repr__(self):
    return '<Estoque {}, {}, {}, {}>'.format(self.produto_nome, self.preco, self.qtd_estoque, self.avaliacao)