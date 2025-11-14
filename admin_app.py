from flask import Flask, request, render_template_string, redirect
import os
from models import SessionLocal, User, Broadcast, init_db
init_db()
app=Flask('admin')
TEMPLATE_LOGIN='''<h2>Mehrozkiyad Admin</h2><form method='POST'><input name='password' placeholder='ADMIN PASSWORD'/><button>Login</button></form>'''
@app.route('/')
def root(): return redirect('/admin')
@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method=='POST':
        if request.form.get('password')==os.environ.get('ADMIN_PASSWORD','change_me'):
            db=SessionLocal(); users=db.query(User).all(); broadcasts=db.query(Broadcast).all(); db.close()
            return render_template_string('<h2>Admin</h2><p>Users: {{n}}</p><form method="POST" action="/admin/broadcast"><input name="title" placeholder="title"/><br/><textarea name="message"></textarea><br/><button>Broadcast</button></form>', n=len(users))
        else:
            return 'Wrong password',403
    return render_template_string(TEMPLATE_LOGIN)
@app.route('/admin/broadcast', methods=['POST'])
def broadcast():
    title=request.form.get('title'); message=request.form.get('message')
    db=SessionLocal(); b=Broadcast(title=title,message=message); db.add(b); db.commit(); db.close()
    return 'Broadcast queued'

if __name__=='__main__': app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
