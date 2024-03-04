from flask import Flask, render_template, request,redirect,session, url_for
from datetime import timedelta
import datetime
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# add static folder
app._static_folder = 'static'
app.secret_key = 'E3lanoTopia@Admin-2024'
app.permanent_session_lifetime = timedelta(days=30)
# make db for all dhashboard
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scholarsync.db'
db = SQLAlchemy(app)

class Dashboard(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  link = db.Column(db.String(100))
  def __init__(self, name, link):
    self.name = name
    self.link = link
@app.route('/login')
def login():
      return render_template('login.html')
# login post
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    if username == 'ScholarSyncApi@Admin' and password == 'E3lanoTopia@Admin-2024':
      session['username'] = username
      session.permanent = True
      return redirect('/')
    else:
        return render_template('login.html', error=True)
@app.route('/')
def index():
  if 'username' not in session:
    return redirect('/login')
  else:
    dashboard = Dashboard.query.all()
    print(dashboard)
    return render_template('index.html', username=session['username'],dateToday=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),Dashboard=dashboard)
# add dashboard 
@app.route('/add_dashboard', methods=['POST'])
def add_dashboard():
  name = request.form['name']
  link = request.form['link']
  dashboard = Dashboard(name=name, link=link)
  db.session.add(dashboard)
  db.session.commit()
  return render_template('add_dashboard.html', ftype='add',success=True)

@app.route('/add_dashboard')
def add_dashboard_page():
  return render_template('add_dashboard.html',ftype='add')
# edit/:id route
@app.route('/edit/<int:id>')
def edit(id):
  dashboard = Dashboard.query.get(id)
  return render_template('add_dashboard.html', ftype='edit',dashboard=dashboard)
# update/:id route
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
  dashboard = Dashboard.query.get(id)
  dashboard.name = request.form['name']
  dashboard.link = request.form['link']
  db.session.commit()
  return redirect('/')
# logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')
if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 