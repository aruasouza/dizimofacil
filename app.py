from flask import Flask,render_template,url_for,redirect,request,abort
from flask_login import login_user, LoginManager, logout_user, current_user, login_required
from user_forms import *
from user_operations import *
import hashlib
from groups import *
from key import key

app = Flask(__name__)

app.config['SECRET_KEY'] = key
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
    def get_temp(self):
        return self._user['temp']
    def get_name(self):
        return self._user['nome']
    
def verify_redirect(next):
    if next in allow_red:
        return next
    return 'home'
    
@app.before_request
def verify_permissions():
    login_needed = request.path in login_required_urls
    special_privilege = request.path in private
    auth = current_user.is_authenticated
    if not login_needed and not special_privilege and not auth:
        return
    if (login_needed or special_privilege) and not auth:
        return redirect(url_for('login',next = request.path[1:]))
    if login_needed and auth:
        if current_user.get_temp():
            return redirect(url_for('novasenha'))
        return
    if special_privilege and auth:
        if current_user.get_temp():
            return redirect(url_for('novasenha'))
        if current_user.get_perfil() not in private[request.path]:
            abort(401)
        return
    if auth and (request.path not in special_case):
        if current_user.get_temp():
            print(current_user._user)
            return redirect(url_for('novasenha'))

@login_manager.user_loader
def load_user(user_id):
    user = get_user(user_id)
    if user:
        return DbUser(user)
    else:
        return None

@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('main.html',name = current_user.get_name())
    return render_template('main.html')

@app.route('/userarea')
@login_required
def userarea():
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
            login_user(DbUser(user))
            return redirect(url_for(next))
        error = 'Usuário ou senha incorretos.'
    return render_template('registerandlogin/login.html',form = form,error = error)

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
                return redirect(url_for('login'))
            else:
                error = 'Já existe uma conta com esse endereço de email.'
        else:
            error = 'As senhas devem ser iguais.'
    return render_template('registerandlogin/register.html',form = form,error = error)

@app.route('/recuperarsenha',methods = ['GET','POST'])
def recuperarsenha():
    form = EmailForm()
    error = None
    if form.validate_on_submit():
        email = form.email.data
        if not verify_email(email):
            restore_password(email)
            return redirect(url_for('inserircodigo',email = email))
        else:
            error = 'Email não cadastrado.'
    return render_template('registerandlogin/recuperarsenha.html',form = form,error = error)

@app.route('/inserircodigo',methods = ['GET','POST'])
def inserircodigo():
    form = CodeForm()
    error = None
    email = request.args.get('email')
    if not email:
        return redirect(url_for('recuperarsenha'))
    if form.validate_on_submit():
        code = form.n.data 
        res = check_verification_code(email,code)
        if res[0] and res[1]:
            id = res[2]
            user = DbUser({'id':id,'perfil':1,'temp':False})
            login_user(user)
            return redirect(url_for('novasenha'))
        if not res[0]:
            error = 'Código inválido.'
        elif not res[1]:
            error = 'Código expirado.'
    return render_template('registerandlogin/inserircodigo.html',form = form,error = error)

@app.route('/novasenha',methods = ['GET','POST'])
def novasenha():
    if not current_user.is_authenticated:
        return redirect(url_for('recuperarsenha'))
    elif not current_user.get_temp():
        abort(401)
    form = RecPassForm()
    error = None
    if form.validate_on_submit():
        senha = hashlib.sha256(form.senha.data.encode()).hexdigest()
        confirm = hashlib.sha256(form.confirm.data.encode()).hexdigest()
        if senha == confirm:
            trocar_senha(current_user.get_id(),senha)
            logout_user()
            return redirect(url_for('login'))
        else:
            error = 'As senhas devem ser iguais.'
    return render_template('registerandlogin/novasenha.html',form = form,error = error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    print(current_user._user)
    return str(private)

@app.route('/minhasigrejas')
@login_required
def minhasigrejas():
    return render_template('minhasigrejas.html')

if __name__ == '__main__':
    app.run(debug = True)