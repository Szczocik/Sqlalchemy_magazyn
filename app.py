from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic

from accountant import manager
from base import init_db

app = Flask(__name__)
Store, Logs, Saldo = init_db(app)
db = SQLAlchemy(app)
# alembic = Alembic()
# alembic.init_app(app)


@app.route("/", methods=["GET", "POST"])
def main():
    mode = request.form.get('mode')
    params = []
    if mode == 'saldo':
        params.append(int(request.form.get('amount')))
        manager_execute(mode, params)
        Saldo.change_saldo(amount=request.form.get('amount'))
    elif mode == 'zakup':
        store = Store(product_name=request.form.get('name'), product_count=request.form.get('count'))
        db.session.add(store)
        db.session.commit()
        params.append(request.form.get('name'))
        params.append(int(request.form.get('count')))
        params.append(int(request.form.get('amount')))
        manager_execute(mode, params)
    elif mode == 'sprzedaz':
        params.append(request.form.get('name'))
        params.append(int(request.form.get('count')))
        params.append(int(request.form.get('amount')))
        manager_execute(mode, params)

    db_saldo = db.session.query(Saldo).first()

    products = {}
    db_products = db.session.query(Store).all()
    for db_product in db_products:
        products[db_product.product_name] = {'count': db_product.product_count, 'price': 0}
    return render_template("index.html", saldo=db_saldo.saldo, store=products)


@app.route("/history/<index_start>/<index_stop>", methods=["GET", "POST"])
@app.route("/history")
def history(index_start=None, index_stop=None):
    logs = db.session.query(Logs).all()
    # manager.logs_read_file()
    # if not index_start:
    #     index_start = 0
    # if not index_stop:
    #     index_stop = len(manager.logs)
    # print(len(manager.logs))
    history = manager.logs[int(index_start): int(index_stop)]

    context = {
        "name": "Adam",
        "start": index_start,
        "stop": index_stop
    }
    return render_template("history.html", history=history, context=context)


def manager_execute(mode, params):
    manager.execute(mode, params)


if __name__ == '__main__':
    manager.read_file()
    app.run()


