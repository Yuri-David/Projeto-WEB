from app import db
from datetime import datetime


class Avaliacao(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  autor = db.Column(db.String(64), index=True)
  nota = db.Column(db.Integer(), index=True)
  comentario = db.Column(db.String(512), index=True)
  timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
  usuario_id = db.Column(db.Integer(), db.ForeignKey('usuario.id'))
  estoque_id = db.Column(db.Integer(), db.ForeignKey('estoque.id'))

  def __repr__(self):
    return '<Avaliacao {}, {}, {}>'.format(self.autor, self.nota, self.comentario)