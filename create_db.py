from project.app import app, db
from project.models import Post

with app.app_context():
  db.create_all() # create database and table
  db.session.commit() # commit changes