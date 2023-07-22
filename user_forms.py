from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, DateField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, Email

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
                             InputRequired(), Length(min=4, max=20)], render_kw={"id": "senha"})
    
    confirm = PasswordField(validators=[
                             InputRequired(), Length(min=4, max=20)], render_kw={"id": "confirm"})

    submit = SubmitField('Criar conta')


class LoginForm(FlaskForm):
    email = EmailField(validators=[
                           InputRequired()], render_kw={"placeholder": "Email"})

    senha = PasswordField(validators=[
                             InputRequired()], render_kw={"placeholder": "Senha"})

    submit = SubmitField('Entrar')