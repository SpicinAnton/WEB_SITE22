from flask import Flask, render_template, redirect
from flask_login import LoginManager
from data import db_session
from forms.user import RegisterForm, LoginForm, TovarForm
from data.users import User, Tovar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/web.db")
    app.run(port=8080, host='127.0.0.1')


login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('glav_str.html')
    # 'WouldBerris'


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            return redirect('/logined')
    return render_template('login.html', form=form)


@app.route('/logined')
def logined():
    return render_template('logined.html')


@app.route('/korzina')
def korzina():
    return render_template('korzina.html')


@app.route('/add')
def add():
    form1 = TovarForm()
    if form1.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Tovar).filter(Tovar.name == form1.name.data).first():
            return render_template('add.html', title='Добавить товар',
                                   form=form1,
                                   message="Такой товар уже есть")
        tovar = Tovar(
            name=form1.name.data,
            name1=form1.name1.data,
            name2=form1.name2.data,
            name3=form1.name3.data,
            prise=form1.prise.data,

        )
        tovar.set_password(form1.name.data)
        db_sess.add(tovar)
        db_sess.commit()
        return redirect('/logined')
    return render_template('add.html', form=form1)
#



if __name__ == '__main__':
    main()
