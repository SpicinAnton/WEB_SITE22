from flask import Flask, render_template, redirect
import flask_login
from flask_login import LoginManager
from data import db_session
from forms.user import RegisterForm
from data.users import User

app = Flask(__name__)


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


# @login_manager.user_loader
# def load_user(user_id):
#    db_sess = db_session.create_session()
#    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    main()
