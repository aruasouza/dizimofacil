from flask import Flask,render_template,url_for,redirect,flash,request,abort
from flask_login import UserMixin, login_user, LoginManager, logout_user, current_user, login_required
from user_forms import LoginForm,RegisterForm
from user_operations import verify_email,create_user,user_login,get_user
import hashlib
from groups import *

app = Flask(__name__)
with open('config/key','r') as f:
    app.config['SECRET_KEY'] = f.read()
login_manager = LoginManager()
login_manager.init_app(app) 

class DbUser:
    def __init__(self, user):
        self._user = user
        self.is_active = True
        self.is_anonymous = False
        self.is_authenticated = True
    def get_id(self):
        return self._user['id']
    def get_perfil(self):
        return self._user['perfil']
    
def verify_redirect(next):
    if next in allow_red:
        return next
    return 'home'
    
@app.before_request
def require_login():
    if request.path in login_required_urls:
        if not current_user.is_authenticated:
            return redirect(url_for('login',next = request.path[1:]))
    if request.path in private: 
        if not current_user.is_authenticated:
            return redirect(url_for('login',next = request.path[1:]))
        if current_user.get_perfil() not in private[request.path]:
            abort(401)

@login_manager.user_loader
def load_user(user_id):
    user = get_user(user_id)
    if user:
        return DbUser(user)
    else:
        return None

@app.route('/')
@login_required
def home():
    return render_template('welcome.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()
    error = None
    next = request.args.get('next')
    next = verify_redirect(next)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        senha = hashlib.sha256(form.senha.data.encode()).hexdigest()
        email = form.email.data
        user = user_login(email,senha)
        if user: 
            flash('Login realizado com sucesso.')
            login_user(DbUser(user))
            flash('Login efetuado com sucesso.')
            return redirect(url_for(next))
        error = 'Usuário ou senha incorretos.'
    return render_template('login.html',form = form,error = error)

@app.route('/register',methods = ['GET','POST'])
def register():
    form = RegisterForm()
    error = None 
    if form.validate_on_submit():
        senha = hashlib.sha256(form.senha.data.encode()).hexdigest()
        confirm = hashlib.sha256(form.confirm.data.encode()).hexdigest()
        nome = form.nome.data
        sobrenome = form.sobrenome.data
        nascimento = form.nascimento.data
        sexo = form.sexo.data
        email = form.email.data
        if senha == confirm:
            if verify_email(email):
                create_user(nome,sobrenome,nascimento,sexo,email,senha)
                flash('Usuário criado com sucesso.')
                return redirect(url_for('login'))
            else:
                error = 'Já existe uma conta com esse endereço de email.'
        else:
            error = 'As senhas devem ser iguais.'
    return render_template('register.html',form = form,error = error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu.')
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/minhasigrejas')
@login_required
def minhasigrejas():
    return render_template('minhasigrejas.html')

if __name__ == '__main__':
    app.run(debug = True)