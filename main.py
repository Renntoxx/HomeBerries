import datetime
import os
from uuid import uuid4

from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.goods import Goods
from data.users import User
from forms.user import RegisterForm, LoginForm
from forms.goods import photos, configure_uploads, patch_request_class
from forms.balance import BalanceFrom
from forms.goods import GoodsForm
from TGBot import start_bot

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['UPLOADED_PHOTOS_DEST'] = os.path.abspath(os.getcwd() + '/static/img/')
configure_uploads(app, photos)
patch_request_class(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    param = {}
    if current_user.is_authenticated:
        param["username"] = current_user.name
        param["exit"] = True
        param["balance"] = current_user.balance
    param['title'] = 'HomeBerries'
    search = request.args.get('search', None)
    if search:
        if search == "@" and current_user.is_authenticated:
            goods = db_sess.query(Goods).filter(Goods.owner == current_user.name)
        else:
            goods = db_sess.query(Goods).filter(
                (Goods.title.contains(search)) & (Goods.sellable == 1))
    else:
        goods = db_sess.query(Goods).filter(Goods.sellable == 1)
    param['goods'] = goods
    param['search'] = search
    return render_template('index.html', **param)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
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


@app.route('/goods', methods=['GET', 'POST'])
@login_required
def add_goods():
    form = GoodsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = Goods()
        if form.photo.data:
            filename = photos.save(form.photo.data, name=uuid4().hex + '.')
            full_filename = f"/static/img/{filename}"
            goods.image_path = full_filename
        else:
            goods.image_path = "/static/images/no-image.png"
        goods.title = form.title.data
        goods.content = form.content.data
        goods.cost = form.cost.data
        goods.owner = current_user.name
        goods.user = current_user
        current_user.goods.append(goods)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('goods.html', title='Добавление товара',
                           form=form, username=current_user.name)


@app.route('/balance', methods=['GET', 'POST'])
@login_required
def balance_change():
    form = BalanceFrom()
    if form.validate_on_submit() and form.balance.data:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(current_user.id == User.id).first()
        user.balance += int(form.balance.data)
        db_sess.commit()
        return redirect('/')
    return render_template('balance.html', title='Пополнение баланса',
                           form=form, username=current_user.name)


@app.route('/goods_buy/<int:goods_id>', methods=['GET', 'POST'])
@login_required
def images_delete(goods_id):
    session = db_session.create_session()
    goods = session.query(Goods).filter(Goods.id == goods_id).first()
    seller = session.query(User).filter(goods.owner == User.name).first()
    buyer = session.query(User).filter(current_user.id == User.id).first()
    if goods:
        if buyer.balance >= goods.cost:
            try:
                seller.balance += goods.cost
                buyer.balance -= goods.cost
                goods.owner = buyer.name
                session.commit()
            except OSError:
                pass
    else:
        abort(404)
    return redirect('/')


@app.route('/goods_sell/<int:goods_id>', methods=['GET', 'POST'])
@login_required
def goods_sell(goods_id):
    session = db_session.create_session()
    goods = session.query(Goods).filter(Goods.id == goods_id).first()
    if goods:
        try:
            goods.sellable = 1
            session.commit()
        except OSError:
            pass
    else:
        abort(404)
    return redirect('/index?search=@')


@app.route('/goods_unsell/<int:goods_id>', methods=['GET', 'POST'])
@login_required
def goods_unsell(goods_id):
    session = db_session.create_session()
    goods = session.query(Goods).filter(Goods.id == goods_id).first()
    if goods:
        try:
            goods.sellable = 0
            session.commit()
        except OSError:
            pass
    else:
        abort(404)
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/hb.db")
    app.run(port=5000, host='127.0.0.1')
    start_bot()


if __name__ == '__main__':
    main()
