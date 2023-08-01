import psycopg2 as pg
import random
import jwt
from jwt.exceptions import DecodeError
from datetime import datetime,timedelta
from mail import send_verification_code
from key import cred,key

mapa_s = {'Masculino':'m','Feminino':'f'}

con = pg.connect(**cred)
cur = con.cursor()

def verify_email(email):
    query = """
            SELECT * FROM usuarios WHERE email=%s;
            """
    sql = cur.mogrify(query,(email,))
    cur.execute(sql)
    if cur.fetchall():
        return False
    return True

def create_user(nome,sobrenome,nascimento,sexo,email,senha):
    query = """
            INSERT INTO usuarios (nome, sobrenome ,nascimento ,sexo, email, senha, perfil) VALUES (%s, %s, %s, %s, %s, %s, 1);
            """
    sql = cur.mogrify(query,(nome,sobrenome,nascimento,mapa_s[sexo],email,senha))
    cur.execute(sql)
    con.commit()

def user_login(email,senha):
    query = """
            SELECT (id, nome, perfil, temp) FROM usuarios WHERE email=%s AND senha=%s;
            """
    sql = cur.mogrify(query,(email,senha))
    cur.execute(sql)
    user = cur.fetchone()
    if user:
        info = user[0][1:-1].split(',')
        query = """
            UPDATE usuarios SET verification=null WHERE email=%s;
            UPDATE usuarios SET temp='false' WHERE email=%s;
            """
        sql = cur.mogrify(query,(email,email))
        cur.execute(sql)
        con.commit()
        return {'id':info[0],'nome':info[1],'perfil':info[2],'temp':info[3]}
    return False

def get_user(id):
    id = int(id)
    query = """
            SELECT (id, nome, perfil, temp) FROM usuarios WHERE id=%s;
            """
    sql = cur.mogrify(query,(id,))
    cur.execute(sql)
    user = cur.fetchone()
    if user:
        info = user[0][1:-1].split(',')
        return {'id':info[0],'nome':info[1],'perfil':info[2],'temp':info[3]}
    return False

def restore_password(email):
    numbers = [str(random.randint(0,9)) for _ in range(4)]
    code = ''.join(numbers)
    time_limit = str(datetime.now() + timedelta(minutes = 10)).split('.')[0]
    encoded_jwt = jwt.encode({'code': code,'time_limit':time_limit}, key, algorithm="HS256")
    query = """
            UPDATE usuarios SET verification=%s WHERE email=%s;
            """
    sql = cur.mogrify(query,(encoded_jwt,email))
    cur.execute(sql)
    con.commit()
    send_verification_code(email,code)

def check_verification_code(email,code):
    format = '%Y-%m-%d %H:%M:%S'
    query = """
            SELECT (id, verification) FROM usuarios WHERE email=%s;
            """
    sql = cur.mogrify(query,(email,))
    cur.execute(sql)
    id,encoded = cur.fetchone()[0][1:-1].split(',')
    print(id,encoded)
    try:
        decoded = jwt.decode(encoded.encode(), key, algorithms=["HS256"])
    except DecodeError:
        decoded = {'code':code,'time_limit':'1999-01-01 00:00:00'}
    res = ((decoded['code'] == code),(datetime.strptime(decoded['time_limit'],format) > datetime.now()),id)
    if res[0]:
        query = """
            UPDATE usuarios SET verification=null WHERE email=%s;
            UPDATE usuarios SET temp='true' WHERE email=%s;
            """
        sql = cur.mogrify(query,(email,email))
        cur.execute(sql)
        con.commit()
    return res

def trocar_senha(user_id,senha):
    query = """
            UPDATE usuarios SET senha=%s WHERE id=%s;
            UPDATE usuarios SET temp='false' WHERE id=%s;
            """
    sql = cur.mogrify(query,(senha,user_id,user_id))
    cur.execute(sql)
    con.commit()

def remove_temp(user_id):
    user_id = int(user_id)
    query = """
            UPDATE usuarios SET temp='false' WHERE id=%s;
            """
    sql = cur.mogrify(query,(user_id,))
    cur.execute(sql)
    con.commit()