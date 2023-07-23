from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, DateField, SelectField, DecimalField
from wtforms.validators import InputRequired, Length, ValidationError, Email

MIN = 4

class RegisterForm(FlaskForm):
    nome = StringField(validators=[
                           InputRequired(), Length(min=2, max=20)], render_kw={"id": "nome"})
    
    sobrenome = StringField(validators=[
                           InputRequired(), Length(min=2, max=20)], render_kw={"id": "sobrenome"})
    
    nascimento = DateField(validators=[
                           InputRequired()], render_kw={"id": "nascimento"})
    
    sexo = SelectField(validators=[
                           InputRequired()],choices = ['Masculino','Feminino'], render_kw={"id": "sexo"})

    email = EmailField(validators=[
                           InputRequired(), Email()], render_kw={"id": "email"})

    senha = PasswordField(validators=[
                             InputRequired(), Length(min=MIN, max=20)], render_kw={"id": "senha"})
    
    confirm = PasswordField(validators=[
                             InputRequired(), Length(min=MIN, max=20)], render_kw={"id": "confirm"})

    submit = SubmitField('Criar conta')


class LoginForm(FlaskForm):
    email = EmailField(validators=[
                           InputRequired()], render_kw={"id": "email"})

    senha = PasswordField(validators=[
                             InputRequired()], render_kw={"id": "senha"})

    submit = SubmitField('Entrar')

class EmailForm(FlaskForm):
    email = EmailField(validators=[
                           InputRequired()], render_kw={"id": "email"})

    submit = SubmitField('Enviar código')

class CodeForm(FlaskForm):
    n = StringField(validators=[
                           InputRequired()], render_kw={"id": "n"})

    submit = SubmitField('Confirmar')

class RecPassForm(FlaskForm):
    senha = PasswordField(validators=[
                             InputRequired(), Length(min=MIN, max=20)], render_kw={"id": "senha"})
    
    confirm = PasswordField(validators=[
                             InputRequired(), Length(min=MIN, max=20)], render_kw={"id": "confirm"})

    submit = SubmitField('Confirmar')

class NovaSenhaForm(FlaskForm):

    atual = PasswordField(validators=[
                             InputRequired(), Length(min=MIN, max=20)], render_kw={"id": "atual"})

    novasenha = PasswordField(validators=[
                             InputRequired(), Length(min=MIN, max=20)], render_kw={"id": "nova"})
    
    confirm = PasswordField(validators=[
                             InputRequired(), Length(min=MIN, max=20)], render_kw={"id": "confirm"})

    submit = SubmitField('Confirmar')