from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

def database_init():
    db.drop_all()
    db.create_all()


# en-til-mange relation: https://www.youtube.com/watch?v=juPQ04_twtA

class Type(db.Model):
    __tablename__ = "types"

    id = db.Column("id", db.Integer, primary_key=True)
    user_type = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='type', lazy=True)

    def __init__(self, user_type):
        self.user_type = user_type


class User(db.Model):
    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<brugerid %r" % self.id


class Status(db.Model):
    __tablename__ = "status"

    id = db.Column("id", db.Integer, primary_key=True)
    status = db.Column(db.String(200), nullable=False)


class Robot(db.Model):
    __tablename__ = "robots"

    id = db.Column("id", db.Integer, primary_key=True)
    ip_name = db.Column(db.String(200), nullable=False)
    status_id = db.Column(db.Integer, nullable=False, default=4) # Default er den status id som robboten får

    def __init__(self, ip_name):
        self.ip_name = ip_name


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column("id", db.Integer, primary_key=True)
    date_ordered = db.Column(db.DateTime, default=datetime.now)
    date_finished = db.Column(db.DateTime, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # status_id = db.Column(db.Integer, nullable=False, default=1) # Default er den status id som ordren får
    # robot_id = db.Column(db.Integer, nullable=False)
    product = db.Column(db.String(200), nullable=False)

    # def __init__(self, product):
    #     self.product = product



@app.route('/api/user/signup', methods=["POST"])
def opret():
    response = request.get_json()
    username = response["username"]
    password = response["password"]
    user_type = response["user_type"]
    print(f"user type:{user_type}")

    found_user_type = Type.query.filter_by(user_type=user_type).first()
    print(type(found_user_type))
    if not found_user_type:
        _type = Type(user_type)
        print("new user type created")
    else:
        _type = found_user_type
        print("found user type")

    found_user = User.query.filter_by(username=username).first()

    if found_user:
        to_return = {"user_exists": True}
        print("user already created")
    else:
        new_user = User(username, password)


        _type.users.append(new_user)
        db.session.add(_type)

        db.session.add(new_user)
        db.session.commit()

        print(new_user.id)
        print(new_user.username)
        print(new_user.password)
        print(new_user.type_id)
        to_return = {"user_created": True}
        print("user created")

    return jsonify(to_return)

@app.route('/api/user/login', methods=["POST"])
def login():
    response = request.get_json()
    username = response["username"]
    password = response["password"]

    found_user = User.query.filter_by(username=username).first()
    if found_user:
        if password == found_user.password:
            to_return = {"username": username, "logged_in": True, "type": found_user.type_id}
            print("logged in")
        else:
            to_return = {"username": username, "logged_in": False, "type": found_user.type_id}
            print("password incorrect")
    else:
        print("user not found")
        to_return = {"logged_in": False}

    return jsonify(to_return)

@app.route("/api/order/new", methods=["POST"])
def new_order():
    response = request.get_json()
    username = response["username"]
    product = response["product"]

    found_user = User.query.filter_by(username=username).first()
    print(f"found user: {type(found_user)}, username: {found_user.username}")

    new_order = Order(product=json.dumps(product), user=found_user)
    print(f"product: {new_order.product}")

    db.session.add(new_order)
    db.session.commit()

    # # print(new_order.id)
    # # print(new_order.product)
    # # print(new_order.user_id)
    to_return = {"order_created": True}

    return jsonify(to_return)



@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

if __name__ == '__main__':
    database_init()
    app.run(debug=True)
