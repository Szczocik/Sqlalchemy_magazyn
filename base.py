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

        @classmethod
        def change_saldo(cls, change, log_line):
            saldo = db.session.query(Saldo).first()
            if not saldo:
                saldo = Saldo(saldo=0)
            if saldo.saldo + change < 0:
                return False
            saldo.saldo += change
            db.session.add(saldo)
            logs = Logs(log=log_line)
            db.session.add(logs)
            db.session.commit()
            return True


    db.create_all()
    return Store, Logs, Saldo
