from flask import Flask, render_template, request, url_for, redirect, flash, session, abort

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"},
        {"name": "О нас", "url": "about"}]


@app.route('/')
def index():
    return render_template('index.html', title='кабан  ', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title='Сайт кабан', menu=menu)





@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        print(request.form)
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
    return render_template('contact.html', title="Обратная связь", menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Страница не найдена", menu=menu), 404


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))

    if request.method == "POST":
        # Use get() method to avoid KeyError if keys are missing
        username = request.form.get('username')
        password = request.form.get('psw')

        if username == "selfedu" and password == "123":
            session['userLogged'] = username
            return redirect(url_for('profile', username=session['userLogged']))

        # If login fails, you may want to add a message to inform the user
        return render_template('login.html', title="Авторизация", menu=menu, error="Invalid credentials")

    return render_template('login.html', title="Авторизация", menu=menu)


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"Пользователь: {username}"



if __name__ == "__main__":
    app.run(debug=True)
