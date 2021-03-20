from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, PasswordField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class DeleteForm(FlaskForm):
  submit = SubmitField('Confirmar Exclusão')

class UsuarioForm(FlaskForm):
  nome = StringField('Nome', validators=[DataRequired()])
  senha = PasswordField('Senha', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired()])
  nacionalidade = SelectField('Nacionalidade', validators=[DataRequired()], choices=[('Brasil'), ('Estados Unidos'), ('Japão'), ('Portugal'), ('China')])
  submit = SubmitField('Salvar')

class LoginForm(FlaskForm):
  email = StringField('E-mail', validators=[DataRequired()])
  senha = PasswordField('Senha', validators=[DataRequired()])
  lembrar = BooleanField("Lembrar de mim")
  submit = SubmitField('Entrar')

class EstoqueForm(FlaskForm):
  produto_nome = StringField('Produto', validators=[DataRequired()])
  produto_dsc = TextAreaField('Descrição', validators=[DataRequired()])
  qtd_estoque = IntegerField('Estoque', validators=[DataRequired()])
  preco = DecimalField('Preço', places = 2, rounding = None, validators=[DataRequired()])
  submit = SubmitField('Salvar')