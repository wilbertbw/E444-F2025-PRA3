import sqlite3
from flask import Flask, g, render_template, request, session, flash, redirect, url_for, abort, jsonify
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy

basedir = Path(__file__).resolve().parent

# configs
DATABASE = "flaskr.db"
USERNAME = "admin"
PASSWORD = "admin"
SECRET_KEY = "ece444_lab3"
SQLALCHEMY_DATABASE_URI = f'sqlite:///{Path(basedir).joinpath(DATABASE)}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)

app.config.from_object(__name__)

db = SQLAlchemy(app)

from project import models

def connect_db(): # connects to database
  rv = sqlite3.connect(app.config["DATABASE"])
  rv.row_factory = sqlite3.Row
  return rv

def init_db(): # create database
  with app.app_context():
    db = get_db()
    with app.open_resource("schema.sql", mode="r") as f:
      db.cursor().executescript(f.read())
    db.commit()

def get_db(): # open database connection
  if not hasattr(g, "sqlite_db"):
    g.sqlite_db = connect_db()
  return g.sqlite_db

@app.teardown_appcontext # close database connection
def close_db(error):
  if hasattr(g, "sqlite_db"):
    g.sqlite_db.close()

@app.route("/")
def index(): # searches database for entries and displays them
  entries = db.session.query(models.Post)
  return render_template('index.html', entries=entries)

@app.route("/login", methods=['GET', 'POST'])
def login(): # user authentication/session management
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('index'))
  return render_template('login.html', error=error)

@app.route("/logout")
def logout(): # user logout/session management
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('index'))

@app.route("/add",  methods=["POST"])
def add_entry(): # add new post to database
  if not session.get('logged_in'):
    abort(401)
  new_entry = models.Post(request.form['title'], request.form['text'])
  db.session.add(new_entry)
  db.session.commit()
  flash('New entry was successfully posted')
  return redirect(url_for('index'))

@app.route("/delete/<post_id>", methods=['GET'])
def delete_entry(post_id): # delete post from database
  result = {'status': 0, 'message': 'Error'}
  try:
    db.session.query(models.Post).filter_by(id=post_id).delete()
    db.session.commit()
    result = {'status': 1, 'message': "Post Deleted"}
    flash('The entry was deleted.')
  except Exception as e:
    result = {'status': 0, 'message': repr(e)}
  return jsonify(result)

if __name__ == "__main__":
  app.run()