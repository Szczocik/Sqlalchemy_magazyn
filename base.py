from flask_sqlalchemy import SQLAlchemy


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza_danych.db'
    db = SQLAlchemy(app)

    class Store(db.Model):
        id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
        product_name = db.Column(db.String(80), unique=True, nullable=False)
        product_count = db.Column(db.Float, nullable=False)




    class Logs(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        log = db.Column(db.String(120), nullable=False)


    class Saldo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        saldo = db.Column(db.Integer, nullable=False)

        @classmethod
        def change_saldo(cls, amount, log_line):
            db_saldo = db.session.query(Saldo).first()
            change = int(amount)
            if not db_saldo:
                db_saldo = Saldo(saldo=0)
            if db_saldo.saldo + change < 0:
                return False
            db_saldo.saldo += change
            db.session.add(db_saldo)
            logs = Logs(log=log_line)
            db.session.add(logs)
            db.session.commit()
            return True

        @classmethod
        def change_saldo_purches(cls, amount, log_line):
            db_saldo = db.session.query(Saldo).first()
            change = int(amount)
            if not db_saldo:
                db_saldo = Saldo(saldo=0)
            if db_saldo.saldo + change < 0:
                return False
            db_saldo.saldo -= change
            db.session.add(db_saldo)
            logs = Logs(log=log_line)
            db.session.add(logs)
            db.session.commit()
            return True

    db.create_all()
    return Store, Logs, Saldo
