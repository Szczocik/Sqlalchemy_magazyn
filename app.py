from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from accountant import manager
from base import init_db

app = Flask(__name__)
Store, Logs, Saldo = init_db(app)
db = SQLAlchemy(app)


@app.route("/", methods=["GET", "POST"])
def main():
    mode = request.form.get('mode')
    params = []
    if mode == 'saldo':
        params.append(int(request.form.get('amount')))
        manager_execute(mode, params)
    elif mode == 'zakup':
        params.append(request.form.get('name'))
        params.append(int(request.form.get('count')))
        params.append(int(request.form.get('amount')))
        manager_execute(mode, params)
    elif mode == 'sprzedaz':
        params.append(request.form.get('name'))
        params.append(int(request.form.get('count')))
        params.append(int(request.form.get('amount')))
        manager_execute(mode, params)

    return render_template("index.html", saldo=manager.saldo, store=manager.store)


@app.route("/history/<index_start>/<index_stop>", methods=["GET", "POST"])
@app.route("/history")
def history(index_start=None, index_stop=None):
    manager.logs_read_file()
    if not index_start:
        index_start = 0
    if not index_stop:
        index_stop = len(manager.logs)
    print(len(manager.logs))
    history = manager.logs[int(index_start): int(index_stop)]

    context = {
        "name": "Adam",
        "start": index_start,
        "stop": index_stop
    }
    return render_template("history.html", history=history, context=context)


def manager_execute(mode, params):
    manager.execute(mode, params)
    # db.session.add(mode, params)
    # db.session.commit()


if __name__ == '__main__':
    manager.read_file()
    app.run()


