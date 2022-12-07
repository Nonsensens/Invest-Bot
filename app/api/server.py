from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import cast, Integer, Float

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'Server for invest bot'


@app.route('/users')
def users():
    users = User.query.order_by(cast(User.account, Float))
    users_all = list()
    for i in users:
        user_v = dict()
        user_v['tg_id'] = i.tg_id
        user_v['name'] = i.name
        user_v['surname'] = i.surname
        user_v['account'] = i.account
        user_v['photo'] = i.photo
        users_all.append(user_v)
    return users_all[::-1]


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        try:
            photo = request.json['photo']
        except:
            photo = 'default'
        user = User(
            name=request.json['name'],
            surname=request.json['surname'],
            photo=photo,
            tg_id=request.json['tg_id'],
        )
        db.session.add(user)
        db.session.commit()
        return Response(status=201)


@app.route('/profile', methods=['GET', 'POST', 'PUT'])
def profile():
    if request.method == 'GET':
        tg_id = request.json['tg_id']
        try:
            user = User.query.filter_by(tg_id=tg_id)[-1]
        except:
            return 'Нет такого пользователя', 404
        data = {'name': user.name,
                'surname': user.surname,
                'account': user.account,
                'photo': user.photo,
                'first_gift': user.first_gift,
                'timer': user.timer
                }
        return data, 200
    if request.method == 'PUT':
        tg_id = request.json['tg_id']
        user = User.query.filter_by(tg_id=tg_id)[-1]
        data = {'name': user.name,
                'surname': user.surname,
                'account': user.account,
                'photo': user.photo,
                'first_gift': user.first_gift,
                'timer': user.timer
                }
        try:
            name = request.json['name']
        except:
            name = data['name']
        try:
            surname = request.json['surname']
        except:
            surname = data['surname']
        try:
            photo = request.json['photo']
        except:
            photo = data['photo']
        try:
            account = request.json['account']
        except:
            account = data['account']
        try:
            first_gift = request.json['first_gift']
        except:
            first_gift = data['first_gift']
        try:
            timer = request.json['timer']
        except:
            timer = data['timer']
        if name != data['name']:
            user.name = name
        if surname != data['surname']:
            user.surname = surname
        if photo != data['photo']:
            user.photo = photo
        if account != data['account']:
            user.account = account
        if first_gift != data['first_gift']:
            user.first_gift = first_gift
        if timer != data['timer']:
            user.timer = timer
        db.session.commit()

        return data, 200


@app.route('/addstock', methods=['GET', 'POST'])
def addstock():
    if request.method == 'POST':
        stock = Stock(
            name=request.json['name'],
            name_off=request.json['name_off'],
            price=request.json['price'],
            price_old=request.json['price_old'],
            tg_id=request.json['tg_id'],
            count=request.json['count']
        )
        db.session.add(stock)
        db.session.commit()
        return Response(status=205)


@app.route('/stocks', methods=['GET', 'PUT', 'POST'])
def stocks():
    if request.method == 'GET':
        stocks = list()
        stock_c = Stock.query.filter_by(tg_id=request.json['tg_id'])
        for i in stock_c:
            data = dict()
            data['name'] = i.name
            data['name_off'] = i.name_off
            data['price'] = i.price
            data['price_old'] = i.price_old
            data['count'] = i.count
            stocks.append(data)
        return stocks, 205
    if request.method == 'PUT':
        stock = Stock.query.filter_by(tg_id=request.json['tg_id'], name_off=request.json['name_off'])[0]
        try:
            price = round(float(request.json['price']), 2)
            stock.price = price
        except:
            pass
        try:
            stock.count = request.json['count']
        except:
            pass
        db.session.commit()
        return {'count': stock.count}, 201
    if request.method == 'POST':
        try:
            count = Stock.query.filter_by(tg_id=request.json['tg_id'], name_off=request.json['name_off'])[0].count
        except:
            count = 0
        return {'count': count}, 201


@app.route('/remove', methods=['GET', 'PUT'])
def remove():
    if request.method == 'PUT':
        tg_id = request.json['tg_id']
        user = User.query.filter_by(tg_id=tg_id)[-1]
        db.session.delete(user)
        db.session.commit()
        return 'успешно'


@app.route('/sellstock', methods=['GET', 'PUT'])
def delete_stock():
    if request.method == 'PUT':
        name = request.json['name']
        stock = Stock.query.filter_by(name=name, tg_id=request.json['tg_id'])[-1]
        db.session.delete(stock)
        db.session.commit()
        return 'успешно'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tg_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    photo = db.Column(db.Text(500), default='default')
    account = db.Column(db.String(100), default=1000)
    first_gift = db.Column(db.String(100), default=False)
    timer = db.Column(db.String(10000), default=0)
    date_of_entrance = db.Column(db.String(100), default=str(datetime.utcnow()))


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tg_id = db.Column(db.String(100))
    name = db.Column(db.String(100))
    name_off = db.Column(db.String(100))
    price = db.Column(db.String(100))
    price_old = db.Column(db.String(100))
    count = db.Column(db.Integer)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(host='217.18.60.9', port=80, debug=False)
