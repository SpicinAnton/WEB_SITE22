from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, current_user, login_required, login_user
from data import db_session
from forms.user import RegisterForm, LoginForm, TovarForm, TovarEditForm
from data.users import User
from data.tovars import Tovar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/web.db")
    app.run(port=8080, host='127.0.0.1')


login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    tovars = db_sess.query(Tovar)
    return render_template('glav_str.html',tovars=tovars)
    # 'WouldBerris'




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
            login_user(user)
            return redirect('/logined')
    return render_template('login.html', form=form)


@app.route('/logined')
@login_required
def logined():
    db_sess = db_session.create_session()
    tovars = db_sess.query(Tovar)
    return render_template('logined.html', tovars=tovars)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = TovarForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        tovar = Tovar(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            user_id=current_user.id
        )
        db_sess.add(tovar)
        db_sess.commit()
        return redirect('/logined')
    return render_template('add.html', form=form)


@app.route('/poisk')
def poisk():
    db_sess = db_session.create_session()
    tovars = db_sess.query(Tovar)
    text = 'телефон'
    return render_template('poisk.html', tovars=tovars, text=text)


@app.route('/my_tovars')
@login_required
def my_tovars():
    db_sess = db_session.create_session()
    tovars = db_sess.query(Tovar).filter(Tovar.user_id == current_user.id)

    return render_template('my_tovars.html', tovars=tovars)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = TovarEditForm()
    db_sess = db_session.create_session()
    tovars = db_sess.query(Tovar).filter(Tovar.id == id).first()
    if request.method == "GET":
        if tovars:
            form.name.data = tovars.name
            form.description.data = tovars.description
            form.price.data = tovars.price
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        tovar = db_sess.query(Tovar).filter(Tovar.id == id).first()
        if tovar:
            tovar.name = form.name.data
            tovar.description = form.description.data
            tovar.price = form.price.data
            db_sess.commit()
            return redirect('/my_tovars')
        else:
            abort(404)

    return render_template('edit.html', form=form, tovars=tovars)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    db_sess = db_session.create_session()
    tovar = db_sess.query(Tovar).filter(Tovar.id == id).first()
    if tovar:
        db_sess.delete(tovar)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/my_tovars')


if __name__ == '__main__':
    main()
