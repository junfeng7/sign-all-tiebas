#!/usr/bin/env python2
#!---coding=utf8---
from contextlib import closing
import hashlib
import urllib
import urllib2
from functools import wraps

from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash,jsonify,json
from json import loads


import MySQLdb
from MySQLdb.cursors import DictCursor

try :
    from bs4 import BeautifulSoup
except :
    from BeautifulSoup import BeautifulSoup
app = Flask(__name__)
app.debug='True'
app.config.from_object("config")
app.secret_key=app.config["SECRET_KEY"]



def connect_db():
    return MySQLdb.connect(host=app.config["DBHOST"],port=app.config["DBPORT"],user=app.config["DBUSER"],passwd=app.config["DBPASSWD"],db=app.config["DBNAME"],charset='utf8')


def init_db():
    with closing(connect_db()) as db:
        with closing(app.open_resource('server.sql',mode='r')) as f:
            with closing(db.cursor(cursorclass=DictCursor)) as cursor:
                cmd=''
                for line in f:
                    if not line:
                        break
                    line=line.strip()
                    if not line or line[0:2]=='--':
                        continue
                    cmd+=line
                    if line[-1]==';':
                        cursor.execute(cmd)
                        cmd=''

        db.commit()


@app.before_request
def before_request():
    g.db=connect_db()
    g.cursor=g.db.cursor(cursorclass=DictCursor)
    user_id=session.get('id')
    username=session.get('name')
    passwd=session.get('passwd')
    email=session.get('email')
    if username and passwd and user_id and email:
        g.cursor.execute("SELECT * FROM users WHERE id=%s AND email=%s AND name=%s AND passwd=%s",(user_id,email,username,passwd))
        g.user=g.cursor.fetchone()
    else:
        g.user=None

@app.teardown_request
def teardown_request(exception):
    g.cursor.close()
    g.db.close()



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is not True or not g.user:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.cursor.execute("SELECT value FROM settings WHERE name='admin'")
        admin=g.cursor.fetchone()['value']
        if g.user['name']!=admin:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/install',methods=['GET','POST'])
def install():
    g.cursor.execute("SHOW TABLES")
    tables=g.cursor.fetchall()
    if len(tables)==4:
        needCreateTable=False
        g.cursor.execute("SELECT * FROM users WHERE name=(SELECT value FROM settings WHERE name='admin')")
        admin=g.cursor.fetchone()
        if admin:
            return redirect('/login')
    else:
        needCreateTable=True
    if request.method=='GET':
        return render_template('install.html')
    if request.method=='POST':
        if needCreateTable:
            init_db()
        admin=request.form.get('username')
        passwd=request.form.get('passwd')
        email=request.form.get('email')
        if not admin or not passwd or not email:
            abort(400)

        g.cursor.execute("INSERT INTO users(email,name,passwd) VALUES(%s,%s,%s)",(email,admin,hashlib.md5(passwd).hexdigest()))
        g.cursor.execute("INSERT INTO settings(name,value) VALUES(%s,%s)",('admin',email))
        g.db.commit()
        return redirect('/login')



@app.route('/sign',methods=['POST'])
def sign():
    if g.user:
        return redirect('/')
    username=request.form.get('username')
    passwd=request.form.get('passwd')
    email=request.form.get('email') # not use
    cookie=request.form.get('cookie')
    if not username or not email or not passwd:
        abort(400)
    g.cursor.execute("SELECT * FROM users WHERE email=%s",email)
    if g.cursor.fetchone():
        return "%s already used." % email
    g.cursor.execute("INSERT INTO users(email,name,cookie,passwd) VALUES(%s,%s,%s,%s)",(email,username,cookie,hashlib.md5(passwd).hexdigest()))
    g.db.commit()
    return redirect('/login')


@app.route('/login',methods=['GET','POST'])
def login():
    if g.user:
        return redirect('/')
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        email=request.form.get('email')
        passwd=request.form.get('passwd')
        if not email or not passwd:
            abort(400)
        g.cursor.execute("SELECT * FROM users WHERE email=%s AND passwd=%s",(email,hashlib.md5(passwd).hexdigest()))
        user=g.cursor.fetchone()
        if not user:
            #return jsonify({'rep':'error'})
            return redirect('/login')
        else:
            session['logged_in']=True
            session['id']=user['id']
            session['email']=user['email']
            session['name']=user['name']
            session['passwd']=user['passwd']
            #return json.jsonify({'rep':'ok'})
            g.cursor.execute("SELECT value FROM settings WHERE name='admin'")
            if g.cursor.fetchone()['value']==email:
                redirect('/admin')
            return redirect('/')


@app.route('/logout')
@login_required
def logout():
    session.pop('name',None)
    session.pop('logged_in',None)
    session.pop('id',None)
    session.pop('email',None)
    session.pop('passwd')
    return redirect('/login')

def tiebaPost(t):
    data={}
    data['ie']='utf=8'
    data['kw']=t['tieba']
    headers={}
    headers['User-Agent']='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36'
    headers['Cookie']=t['cookie']
    geturl=app.config['TIEBAURL']+t['tieba'].decode('utf-8').encode('gbk')
    getreq=urllib2.Request(url=geturl,headers=headers)
    soup=BeautifulSoup(urllib2.urlopen(getreq).read())
    data['tbs']=soup.body.find('script').string.split('"')[1].encode('utf-8')
    postreq=urllib2.Request(url=app.config['SIGNURL'],data=data,headers=headers)
    postres=urllib2.urlopen(postreq).read()
    print postres


    
    

@app.route('/',methods=['GET','POST'])
@login_required
def index():
    if request.method=='GET':
        g.cursor.execute("SELECT cookie,tieba FROM users,tiebas_users,tiebas WHERE users.id=%s AND users.id=user_id AND tieba_id=tiebas.id",g.user['id'])
        tiebas=g.cursor.fetchall()
        return render_template('index.html',tiebas=tiebas)
    if request.method=='POST':

        return "doen"

@app.route('/work',methods=['POST'])
def work():
    email=request.form.get('email')
    passwd=request.form.get('passwd')
    g.cursor.execute("SELECT value FROM settings WHERE name='admin' AND value=(SELECT email FROM users WHERE email=%s AND passwd=%s)",(email,passwd));
    if not g.cursor.fetchone():
        abort(400)
    g.cursor.execute("SELECT cookie,tieba FROM users,tiebas_users,tiebas WHERE users.id=user_id AND tieba_id=tiebas.id")
    tiebas=g.cursor.fetchall()
    for t in tiebas:
        tiebaPost(t)
    return "done"

@app.route('/check')
def check():
    return "to do"

        




@app.route('/admin',methods=['GET','POST'])
@login_required
@admin_required
def admin():
    if request.method=='GET':
        g.cursor.execute("SELECT * FROM users WHERE name!=%s",g.user['name'])
        users=g.cursor.fetchall()
        return render_template('admin.html',users=users)




@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method=='GET':
        return render_template('settings.html')
    if request.method=='POST':
        oldpasswd=request.form.get('oldpasswd')
        newpasswd=request.form.get('newpasswd')
        if not oldpasswd or not newpasswd:
            abort(400)
        if oldpasswd!=newpasswd:
            g.cursor.execute("UPDATE users SET passwd=%s WHERE name=%s AND passwd=%s",(newpasswd,g.user['name'],hashlib.md5(oldpasswd).hexdigest()))
        g.db.commit()
        return redirect('/settings')



#from bae.core.wsgi import WSGIApplication

#application = WSGIApplication(app)

if __name__ == '__main__':
    app.run()
