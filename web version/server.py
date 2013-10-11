#!/usr/bin/env python2
#!---coding=utf8---
from contextlib import closing
import hashlib
import urllib
import urllib2
import time
from functools import wraps
import itertools

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
        with closing(app.open_resource('tieba.sql',mode='r')) as f:
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
        g.cursor.execute("SELECT value FROM settings WHERE name='admin'")
        admin=g.cursor.fetchone()
        if admin:
            g.admin=admin['value']
        else:
            g.admin=None
        return f(*args, **kwargs)
    return decorated_function



def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user['email']!=g.admin or not g.admin: 
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/install',methods=['GET','POST'])
def install():
    g.cursor.execute("SHOW TABLES")
    tables=g.cursor.fetchall()
    if len(tables)==4:
        needCreateTable=False
        g.cursor.execute("SELECT * FROM users WHERE email=(SELECT value FROM settings WHERE name='admin')")
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
    email=request.form.get('email')
    if not username or not email or not passwd:
        abort(400)
    g.cursor.execute("SELECT * FROM users WHERE email=%s",email)
    if g.cursor.fetchone():
        return jsonify({'rep':'error','data':"%s already used." % email})
    g.cursor.execute("INSERT INTO users(email,name,passwd) VALUES(%s,%s,%s)",(email,username,hashlib.md5(passwd).hexdigest()))
    g.db.commit()
    return jsonify({'rep':'ok','data':'successfully signed.'})


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
            return jsonify({'rep':'error','data':'email or passwd not correct'})
        else:
            session['logged_in']=True
            session['id']=user['id']
            session['email']=user['email']
            session['name']=user['name']
            session['passwd']=user['passwd']
            url='/'
            g.cursor.execute("SELECT value FROM settings WHERE name='admin'")
            if g.cursor.fetchone()['value']==email:
                url='/admin'
            return jsonify({'rep':'ok','data':'login successfully.','url':url})


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
    data['kw']=t['tieba'].encode('utf8')
    headers={}
    headers['User-Agent']='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36'
    headers['Cookie']=t['cookie']
    indexurl=app.config['TIEBAURL']+t['tieba'].encode('gbk')
    request=urllib2.Request(url=indexurl,headers=headers)
    soup=BeautifulSoup(urllib2.urlopen(request).read())
    data['tbs']=soup.body.find('script').string.split('"')[1].encode('utf-8')
    request=urllib2.Request(url=app.config['SIGNURL'],data=urllib.urlencode(data),headers=headers)
    response=urllib2.urlopen(request)
    meg=response.read()
    return meg




@app.template_filter('strftime')
def _jinja2_strftime(date,fmt=None):
    if not fmt:
        _format="%Y-%m-%d %H:%M:%S"
    else:
        _format=fmt
    date=date if date else time.time()
    return time.strftime(_format,time.localtime(date))

    

@app.route('/',methods=['GET','POST'])
@login_required
def index():
    if request.method=='GET':
        g.cursor.execute("SELECT message,tieba FROM users,tiebas_users,tiebas WHERE users.id=%s AND users.id=user_id AND tieba_id=tiebas.id",g.user['id'])
        tiebas=g.cursor.fetchall()
        for t in tiebas:
            if t['message']:
                t['message']=loads(t['message'])
        return render_template('index.html',tiebas=tiebas)
    if request.method=='POST':
        action=request.args.get('action')
        tiebas=loads(request.form.get('tiebas'))
        if action=='add':
            add={}
            i=0
            for t in tiebas:
                g.cursor.execute("SELECT id FROM tiebas WHERE tieba=%s",t)
                tieba_id=g.cursor.fetchone()
                if tieba_id:
                    tieba_id=tieba_id['id']
                    g.cursor.execute("SELECT * FROM tiebas_users WHERE tieba_id=%s AND user_id=%s",(tieba_id,g.user['id']))
                    if g.cursor.fetchone():
                        continue
                    g.cursor.execute("INSERT INTO tiebas_users(tieba_id,user_id) VALUES(%s,%s)",(tieba_id,g.user['id']))
                else:
                    g.cursor.execute("INSERT INTO tiebas(tieba) VALUES(%s)",t)
                    g.cursor.execute("SELECT id FROM tiebas WHERE tieba=%s",t)
                    tieba_id=g.cursor.fetchone()['id']
                    g.cursor.execute("INSERT INTO tiebas_users(tieba_id,user_id) VALUES(%s,%s)",(tieba_id,g.user['id']))
                add[i]=t
                i+=1
            add['c']=i
            if i==0:
                return jsonify({'rep':'error','data':'you have added prior.'})
            g.db.commit()
            return jsonify({'rep':'ok','data':add})

        if action=='delete':
            deleted={}
            i=0
            for t in tiebas:
                g.cursor.execute("SELECT id FROM tiebas WHERE tieba=%s",t)
                tieba_id=g.cursor.fetchone()
                if not tieba_id:
                    continue
                tieba_id=tieba_id['id']
                g.cursor.execute("DELETE FROM tiebas_users WHERE user_id=%s AND tieba_id=%s",(g.user['id'],tieba_id))

                g.cursor.execute("SELECT id FROM tiebas,tiebas_users WHERE tiebas.id=tieba_id")
                tiebasHasUser=g.cursor.fetchall()
                tiebasHasUser=[tu['id'] for tu in tiebasHasUser]
                args=','.join(itertools.repeat('%s',len(tiebasHasUser)))
                sql="DELETE FROM tiebas WHERE id NOT IN (%s)" % args
                g.cursor.execute(sql,tiebasHasUser)
                deleted[i]=t
                i+=1
            deleted['c']=i
            if i==0:
                return jsonify({'rep':'error','data':'no tieba deleted.'})
            g.db.commit()
            return jsonify({'rep':'ok','data':deleted})
        if action=='sign':
            signed={}
            i=0
            for t in tiebas:
                g.cursor.execute("SELECT id FROM tiebas WHERE tieba=%s",t)
                tieba_id=g.cursor.fetchone()
                if not tieba_id:
                    continue
                tieba_id=tieba_id['id']
                g.cursor.execute("SELECT * FROM tiebas_users WHERE tieba_id=%s AND user_id=%s",(tieba_id,g.user['id']))
                tieba_user=g.cursor.fetchone()
                lastmeg=None
                if tieba_user:
                    lastmeg=tieba_user['message']
                if lastmeg:
                    lastmeg=loads(lastmeg)
                    if lastmeg['error'] and lastmeg['no']!=4:
                        continue
                    if not lastmeg['error'] and lastmeg['no']==0:
                        uinfo=lastmeg['data']['uinfo']
                        lastsignday=time.strftime("%Y-%m-%d",time.localtime(uinfo['sign_time']))
                        today=time.strftime("%Y-%m-%d",time.localtime())
                        if lastsignday==today:
                            continue
                todaymeg=tiebaPost({'cookie':g.user['cookie'],'tieba':t})
                g.cursor.execute("UPDATE tiebas_users SET message=%s WHERE tieba_id=%s AND user_id=%s",(todaymeg,tieba_id,g.user['id']))
                signed[i]={'tieba':t,'meg':loads(todaymeg)}
                i+=1

            signed['c']=i
            if i==0:
                return jsonify({'rep':'error','data':'no tieba signed.'})
            g.db.commit()
            return jsonify({'rep':'ok','data':signed})






@app.route('/cron',methods=['POST'])
def cron():
    db=connect_db()
    cursor=db.cursor(cursorclass=DictCursor)
    email=request.form.get('email')
    passwd=request.form.get('passwd')
    cursor.execute("SELECT value FROM settings WHERE name='admin' AND value=(SELECT email FROM users WHERE email=%s AND passwd=%s)",(email,hashlib.md5(passwd).hexdigest()));
    if not cursor.fetchone():
        abort(400)
    cursor.execute("SELECT cookie,tieba_id,user_id,tieba FROM users,tiebas_users,tiebas WHERE cookie IS NOT NULL AND users.id=user_id AND tieba_id=tiebas.id")
    tiebas=cursor.fetchall()
    tdict={}
    i=0
    for t in tiebas:
      	tdict[i]=t
      	i+=1
        meg=tiebaPost(t)
        cursor.execute("UPDATE tiebas_users SET message=%s WHERE tieba_id=%s AND user_id=%s",(meg,t['tieba_id'],t['user_id']))
    db.commit()
    cursor.close()
    db.close()
    return "hello,world."

@app.route('/check')
def check():
    return "nothing to check"

        




@app.route('/admin',methods=['GET','POST'])
@login_required
@admin_required
def admin():
    if request.method=='GET':
        g.cursor.execute("SELECT * FROM users WHERE name!=%s",g.user['name'])
        users=g.cursor.fetchall()
        return render_template('admin.html',users=users)
    if request.method=='POST':
        users=loads(request.form.get('users'))
        deleted={}
        i=0
        for u in users:
            g.cursor.execute("SELECT id FROM users WHERE id=%s",u)
            uid=g.cursor.fetchone()
            if not uid:
                continue
            uid=uid['id']
            g.cursor.execute("DELETE FROM tiebas_users WHERE user_id=%s",u)
            #g.cursor.execute("DELETE FROM tiebas WHERE id NOT IN (SELECT tid FROM (SELECT id as tid FROM tiebas,tiebas_users WHERE tiebas.id=tieba_id) AS t)")
            g.cursor.execute("SELECT id FROM tiebas,tiebas_users WHERE tiebas.id=tieba_id")
            tiebasHasUser=g.cursor.fetchall()
            if tiebasHasUser:
                tiebasHasUser=[t['id'] for t in tiebasHasUser]
                args=','.join(itertools.repeat('%s',len(tiebasHasUser)))
                sql="DELETE FROM tiebas WHERE id NOT IN (%s)" % args
                g.cursor.execute(sql,tiebasHasUser)
            else:
                g.cursor.execute("DELETE FROM tiebas WHERE 1")
            g.cursor.execute("DELETE FROM users WHERE id=%s",u)
            deleted[i]=u
            i+=1
        deleted['c']=i
        if i==0:
            return jsonify({'rep':'error'})
        g.db.commit()
        return jsonify({'rep':'ok','data':deleted})




@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method=='GET':
        return render_template('settings.html')
    if request.method=='POST':
        action=request.form.get('f')
        if action=='changeProfile':
            newname=request.form.get('newname') if request.form.get('newname') else g.user['name']
            oldpasswd=request.form.get('oldpasswd')
            newpasswd=request.form.get('newpasswd') if request.form.get('newpasswd') else g.user['passwd']
            if not oldpasswd:
                abort(400)
            g.cursor.execute("UPDATE users SET name=%s,passwd=%s WHERE email=%s AND passwd=%s",(newname,hashlib.md5(newpasswd).hexdigest(),g.user['email'],hashlib.md5(oldpasswd).hexdigest()))
            g.db.commit()
            return jsonify({'ok':'successfully changed.'})
        if action=='addCookie':
            cookie=request.form.get('cookie')
            if not cookie:
                abort(400)
            g.cursor.execute("UPDATE users SET cookie=%s WHERE email=%s AND passwd=%s",(cookie,g.user['email'],g.user['passwd']))
            g.db.commit()
            return jsonify({'ok':'updated Cookie.'})
        return jsonify({'error':'no post server of this way.'})


@app.route('/about')
def about():
    return render_template('about.html')


#from bae.core.wsgi import WSGIApplication

#application = WSGIApplication(app)

if __name__ == '__main__':
    app.run()
