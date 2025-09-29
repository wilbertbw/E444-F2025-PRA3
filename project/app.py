import sqlite3
from flask import Flask, g

DATABASE = "flaskr.db"

app = Flask(__name__)

app.config.from_object(__name__)

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
def hello():
  return "Hello, World!"

if __name__ == "__main__":
  app.run()