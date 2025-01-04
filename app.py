from flask import Flask, render_template, request, flash, session, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qw@@1981@@qw-qw@@1981@@qw'

menu = [
    {"name": "Install", "url": "install-flask"},
    {"name": "First App", "url": "first-app"},
    {"name": "Feedback", "url": "feedback"}
]


@app.route('/')
def index():
    return render_template('index.html', title='About Flask', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title='About site', menu=menu)


@app.route('/profile/<username>')
def profile(username):
    return render_template('profile.html', username=username, title='About User')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'userLoggedIn' in session:
        return redirect(url_for('profile', username=session['userLoggedIn']))
    elif request.method == 'POST' and request.form['username'] == 'roma' and request.form['password'] == '123':
        session['userLoggedIn'] = request.form['username']
        return redirect(url_for('profile', username=session['userLoggedIn']))
    return render_template('login.html', title='Authorization', menu=menu)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        flash('Message has been send', category='success')
    return render_template('feedback.html', title='Feedback', menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('response_404.html', title='Page was not found', menu=menu), 404


if __name__ == '__main__':
    app.run(debug=True)
