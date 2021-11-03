from flask_sqlalchemy import SQLAlchemy


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza_danych.db'
    db = SQLAlchemy(app)

    class Store(db.Model):
        id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
        product_name = db.Column(db.String(80), unique=True, nullable=False)
        product_count = db.Column(db.Float, unique=True, nullable=False)


    class Logs(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        log = db.Column(db.String(120), nullable=False)


    class Saldo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        saldo = db.Column(db.Integer, nullable=False)

    db.create_all()
    return Store, Logs, Saldo
