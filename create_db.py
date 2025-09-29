from project.app import app, db

with app.app_context():
    db.create_all()  # create database and table
    db.session.commit()  # commit changes
