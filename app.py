from flask import Flask, render_template, request, flash, session, redirect, url_for, abort, g
from FDataBase import FDataBase
import sqlite3
import os


DATABASE = '/tmp/flask.db'
DEBUG = True
SECRET_KEY = 'qw@@1981@@qw-qw@@1981@@qw'

app = Flask(__name__)
app.config.from_object(__name__)

a = dict(DATABASE=os.path.join(app.root_path, 'flask.db'))
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flask.db')))


# функции работы с БД:
def connect_db():
    connect = sqlite3.connect(app.config['DATABASE'])
    connect.row_factory = sqlite3.Row
    return connect


def create_db():
    db = connect_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext  # декоратор - закрываем соединение с БД, если оно было установлено
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()
###


@app.route('/')
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', title='About Flask', menu=dbase.get_menu())


@app.route('/about')
def about():
    return render_template('about.html', title='About site', menu=[])


@app.route('/profile/<username>')
def profile(username):
    if 'userLoggedIn' not in session or session['userLoggedIn'] != username:
        abort(401)
    return render_template('profile.html', username=username, title='About User')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'userLoggedIn' in session:
        return redirect(url_for('profile', username=session['userLoggedIn']))
    elif request.method == 'POST' and request.form['username'] == 'roma' and request.form['password'] == '123':
        session['userLoggedIn'] = request.form['username']
        return redirect(url_for('profile', username=session['userLoggedIn']))
    return render_template('login.html', title='Authorization', menu=[])


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        flash('Message has been send', category='success')
    return render_template('feedback.html', title='Feedback', menu=[])


@app.errorhandler(404)
def page_not_found(error):
    return render_template('response_404.html', title='Page was not found', menu=[]), 404


if __name__ == '__main__':
    app.run(debug=True)
