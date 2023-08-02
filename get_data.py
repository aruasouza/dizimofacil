import psycopg2 as pg
from datetime import date
from key import cred

con = pg.connect(**cred)
cur = con.cursor()

def get_calendar(year):
    first = date(year,1,1)
    last = date(year,12,31)
    query = """
            SELECT * FROM calendario WHERE dia>=%s AND dia<=%s;
            """
    sql = cur.mogrify(query,(first,last))
    cur.execute(sql)
    return cur.fetchall()

def get_day(day):
    query = """
            SELECT * FROM calendario WHERE dia=%s;
            """
    sql = cur.mogrify(query,(day,))
    cur.execute(sql)
    return cur.fetchall()

def get_all_church_info(church_id):
    query = """
            SELECT * FROM igrejas WHERE id=%s;
            """
    sql = cur.mogrify(query,(church_id,))
    cur.execute(sql)
    info = cur.fetchone()
    query = """
            SELECT * FROM horariosMissa WHERE id=%s;
            """
    sql = cur.mogrify(query,(church_id,))
    cur.execute(sql)
    horariosMissa = cur.fetchall()
    query = """
            SELECT * FROM horariosConfissao WHERE id=%s;
            """
    sql = cur.mogrify(query,(church_id,))
    cur.execute(sql)
    horariosConf = cur.fetchall()
    return {'info':info,'missa':horariosMissa,'conf':horariosConf}