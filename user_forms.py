from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo

class RegisterForm(FlaskForm):
    nome = StringField(validators=[
                           InputRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Nome"})

    email = EmailField(validators=[
                           InputRequired(), Email()], render_kw={"placeholder": "Email"})

    senha = PasswordField(validators=[
                             InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Senha"})
    
    confirm = PasswordField(validators=[
                             InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Confirmar senha"})

    submit = SubmitField('Criar conta')


class LoginForm(FlaskForm):
    email = EmailField(validators=[
                           InputRequired()], render_kw={"placeholder": "Email"})

    senha = PasswordField(validators=[
                             InputRequired()], render_kw={"placeholder": "Senha"})

    submit = SubmitField('Entrar')