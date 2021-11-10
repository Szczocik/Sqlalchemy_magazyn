from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


from accountant import manager
from base import init_db

app = Flask(__name__)
Store, Logs, Saldo = init_db(app)
db = SQLAlchemy(app)



@app.route("/", methods=["GET", "POST"])
def main():
    context = {
        'error_saldo':'',
        'error_zakup':'',
        'error_sprzedaz':'',
    }
    mode = request.form.get('mode')
    if mode == 'saldo':
        amount = request.form.get('amount')
        log = f"Zmiana saldo o: {amount}"
        if not Saldo.change_saldo(amount=amount, log_line=log):
            context['error_saldo'] = 'Nie masz wystarczających środków na koncie!'
    elif mode == 'zakup':
        product = request.form.get('name')
        product_count = int(request.form.get('count'))
        product_price = float(request.form.get('amount'))
        amount = product_price * product_count
        log = f'Dokonano zakupu produktu: {product} w ilości {product_count} sztuk, w cenie jednostkowej {product_price} zł.'
        if not Saldo.change_saldo_purches(amount=amount, log_line=log):
            db_saldo = db.session.query(Saldo).first()
            context['error_zakup'] = f'Cena za towary ({amount}) przekracza wartość salda {db_saldo.saldo}'
        else:
            store = db.session.query(Store).filter(Store.product_name==product).first()
            if not store:
                store = Store(product_name=product, product_count=request.form.get('count'))
            store.product_count += product_count
            db.session.add(store)
            db.session.commit()
    elif mode == 'sprzedaz':
        product = request.form.get('name')
        product_count = int(request.form.get('count'))
        product_price = float(request.form.get('amount'))
        amount = product_price * product_count
        log = f"Dokonano sprzedaży produktu: {product} w ilości {product_count} sztuk, o cenie jednostkowej {product_price} zł."
        store = db.session.query(Store).filter(Store.product_name==product).first()
        if not store:
            context['error_sprzedaz'] = 'Produktu nie ma w magazynie!'
        elif store.product_count < product_count:
            context['error_sprzedaz'] = 'Brak wystarczającej ilości towaru!'
        else:
            Saldo.change_saldo(amount=amount, log_line=log)
            store.product_count -= product_count
            db.session.add(store)
            db.session.commit()

    db_saldo = db.session.query(Saldo).first()
    if not db_saldo:
        db_saldo = Saldo(saldo=0)

    products = {}
    db_products = db.session.query(Store).all()
    for db_product in db_products:
        products[db_product.product_name] = {'count': db_product.product_count, 'price': 0}

    context['saldo'] = db_saldo.saldo
    context['store'] = products
    return render_template("index.html", **context)


@app.route("/history/<index_start>/<index_stop>", methods=["GET", "POST"])
@app.route("/history")
def history(index_start=None, index_stop=None):

    if not index_start:
        index_start = 0
    if not index_stop:
        index_stop = db.session.query(Logs.id).count()
    history = db.session.query(Logs).filter(Logs.id >= index_start).filter(Logs.id <= index_stop).all()

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


