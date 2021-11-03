from flask_sqlalchemy import SQLAlchemy


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza_danych.db'
    db = SQLAlchemy(app)

    class Store(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        product_name = db.Column(db.String(80), unique=True, nullable=False)
        product_count = db.Column(db.Float, nullable=False)
        db.session.add(app)
        db.session.commit()

    class Logs(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        log = db.Column(db.String(120), nullable=False)
        db.session.add(app)
        db.session.commit()

    class Saldo(db.Model):
        saldo = db.Column(db.Integer, nullable=False)
        db.session.add(app)
        db.session.commit()

    return Store, Logs, Saldo
