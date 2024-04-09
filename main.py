from flask import Flask, render_template
import flask_login
from flask_login import LoginManager
from data import db_session
from data.users import User

db_session.global_init("db/blogs.db")
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('glav_str.html')
    #'WouldBerris'


@app.route('/about')
def about():
    return render_template('about.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
