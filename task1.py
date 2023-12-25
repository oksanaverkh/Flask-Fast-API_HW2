# Создать страницу, на которой будет форма для ввода имени и электронной почты,
# при отправке которой будет создан cookie-файл с данными пользователя,
# а также будет произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя.
# На странице приветствия должна быть кнопка «Выйти»,
# при нажатии на которую будет удалён cookie-файл с данными пользователя и произведено перенаправление на страницу ввода имени и электронной почты

from flask import Flask, render_template, request, make_response, url_for, redirect


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('form_name.html')


@app.post('/login/')
def login():
    login = request.form.get('username')
    email = request.form.get('email')

    response = make_response(redirect(url_for('login_success', name=login)))
    response.headers['new_head'] = 'New value'
    response.set_cookie('username', login)
    response.set_cookie('email', email)

    return response


@app.route('/success/<name>')
def login_success(name: str):
    return render_template('greeting.html', context=name)


@app.route('/getcookie/')
def getcookie():
    name = request.cookies.get('username')
    email = request.cookies.get('email')
    if (not name or name == None) and (not email or email == None):
        return f"Cookie не установлены"

    return f"Значение cookie: имя: {name}, электронная почта: {email}"


@app.route('/del_cookie', methods=['GET'])
def del_cookie():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('username')
    response.delete_cookie('email')
    return response


if __name__ == "__main__":
    app.run(debug=True)
