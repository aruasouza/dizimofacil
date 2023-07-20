import psycopg2 as pg
import json

with open('config/database_info.json','r') as f:
    cred = json.load(f)

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

def create_user(nome,email,senha):
    query = """
            INSERT INTO usuarios (nome, email, senha, perfil) VALUES (%s, %s, %s, 1);
            """
    sql = cur.mogrify(query,(nome,email,senha))
    cur.execute(sql)
    con.commit()
    return 'Sucesso'

def user_login(email,senha):
    query = """
            SELECT (id, perfil) FROM usuarios WHERE email=%s AND senha=%s;
            """
    sql = cur.mogrify(query,(email,senha))
    cur.execute(sql)
    user = cur.fetchone()
    if user:
        info = user[0][1:-1].split(',')
        return {'id':info[0],'perfil':info[1]}
    return False

def get_user(id):
    id = int(id)
    query = """
            SELECT (id, perfil) FROM usuarios WHERE id=%s;
            """
    sql = cur.mogrify(query,(id,))
    cur.execute(sql)
    user = cur.fetchone()
    if user:
        info = user[0][1:-1].split(',')
        return {'id':info[0],'perfil':info[1]}
    return False