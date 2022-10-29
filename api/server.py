from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'Server for invest bot'


@app.route('/users')
def users():
    users = User.query.order_by('id')
    users_v = ''
    for i in users:
        users_v += str(f'username: {i.username}, password: {i.password}, name: {i.name}, surname: {i.surname}') + "              "
    return users_v


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        user = User(
            username=request.json['username'],
            password=request.json['password'],
            name=request.json['name'],
            surname=request.json['surname'],
            status=request.json['status'],
            photo=request.json['photo'],
            tg_id=request.json['tg_id'],

        )

        db.session.add(user)
        db.session.commit()
        return Response(status=201)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                return Response(status=201)
            else:
                return Response(status=200)
        else:
            return Response(status=200)


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
                'status': user.status,
                'account': user.account,
                'photo': user.photo
                }
        return data, 200
    if request.method == 'PUT':
        tg_id = request.json['tg_id']
        user = User.query.filter_by(tg_id=tg_id)[-1]
        data = {'name': user.name,
                'surname': user.surname,
                'status': user.status,
                'account': user.account,
                'photo': user.photo
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
            status = request.json['status']
        except:
            status = data['status']
        if name != data['name']:
            user.name = name
        if surname != data['status']:
            user.surname = surname
        if photo != data['photo']:
            user.photo = photo
        if status != data['status']:
            user.status = status
        db.session.commit()

        return data, 200


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    photo = db.Column(db.Text(500))
    status = db.Column(db.String(500))
    tg_id = db.Column(db.String(100))
    account = db.Column(db.String(100), default=0)
    date_of_entrance = db.Column(db.String(100), default=str(datetime.utcnow()))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(port=5050, debug=False)
