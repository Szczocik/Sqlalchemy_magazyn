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
        # params.append(int(request.form.get('amount')))
        # manager_execute(mode, params)
        amount = request.form.get('amount')
        log = f"Zmiana saldo o: {amount}"
        Saldo.change_saldo(amount=amount, log_line=log)
    elif mode == 'zakup':
        product = request.form.get('name')
        product_count = int(request.form.get('count'))
        product_price = float(request.form.get('amount'))
        amount = product_price * product_count
        log = f'Dokonano zakupu produktu: {product} w ilości {product_count} sztuk, w cenie jednostkowej {product_price} zł.'
        if Saldo.change_saldo(amount=amount, log_line=log):
            store = db.session.query(Store).filter(product_name=product).first()
            if not store:
                store = Store(product_name=request.form.get('name'), product_count=0)

            store.product_count += product_count
            db.session.add(store)
            db.session.add(log)
            db.session.commit()
    elif mode == 'sprzedaz':
        product = request.form.get('name')
        product_count = int(request.form.get('count'))
        product_price = float(request.form.get('amount'))
        log = f"Dokonano sprzedaży produktu: {product} w ilości {product_count} sztuk, o cenie jednostkowej {product_price} zł."
        store = db.session.query(Store).filter(product_name=product).first()
        if store:
            store.product_count -= product_count
            db.session.add(store)
            db.session.add(log)
            db.session.commit()



    db_saldo = db.session.query(Saldo).first()
    if not db_saldo:
        db_saldo = Saldo(saldo=0)

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


