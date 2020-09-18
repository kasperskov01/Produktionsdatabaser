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

    db.session.add(Status(status="Bestilt"))
    db.session.add(Status(status="Produceret"))
    db.session.add(Status(status="Leveret"))
    db.session.add(Status(status="Slettet"))

    robot_available = Status(status="Robot ledig")
    db.session.add(robot_available)
    db.session.add(Status(status="Robot ikke ledig"))

    db.session.add(Robot(ip_name="10.130.58.14", status=robot_available))
    db.session.add(Robot(ip_name="10.130.58.13", status=robot_available))
    db.session.add(Robot(ip_name="10.130.58.12", status=robot_available))
    db.session.add(Robot(ip_name="10.130.58.11", status=robot_available))

    db.session.commit()


# en-til-mange relation: https://www.youtube.com/watch?v=juPQ04_twtA

"""
En til mange relation med flask sqlalchemy

lav dette relationship, på den tabel som er "en" i en til mange relationen.
users = db.relationship('User', backref='type', lazy=True)

'User' er her python klassen som bruges til at bygge "users" tabellen

backref='type' definerer hvordan man skal lave relationen når man laver et nyt user objekt.
Man giver en bruger en type således "User(type=type_objekt)", hvor type_objekt er lavet med Type()
"""

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
    orders = db.relationship("Order", backref="status", lazy=True)
    robots = db.relationship("Robot", backref="status", lazy=True)

class Robot(db.Model):
    __tablename__ = "robots"

    id = db.Column("id", db.Integer, primary_key=True)
    ip_name = db.Column(db.String(200), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False) # Default er den status id som robboten får
    orders = db.relationship("Order", backref="robot", lazy=True)



class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column("id", db.Integer, primary_key=True)
    date_ordered = db.Column(db.DateTime, default=datetime.now)
    date_finished = db.Column(db.DateTime, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    robot_id = db.Column(db.Integer, db.ForeignKey('robots.id'), nullable=False)
    product = db.Column(db.String(200), nullable=False)


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
    status = "Bestilt"
    robot = "10.130.58.14"

    found_user = User.query.filter_by(username=username).first()
    if not found_user:
        to_return = {"order_created": False}
        return jsonify(to_return)

    found_status = Status.query.filter_by(status=status).first()
    found_robot = Robot.query.filter_by(ip_name=robot).first()
    new_order = Order(product=json.dumps(product), user=found_user, status=found_status, robot=found_robot)

    db.session.add(new_order)
    db.session.commit()

    to_return = {"order_created": True}
    return jsonify(to_return)

@app.route("/api/order/get", methods=["POST"])
def get_orders():
    response = request.get_json()
    username = response["username"]

    order_list = []

    found_user = User.query.filter_by(username=username).first()
    if not found_user:
        return jsonify({"orders": order_list})
    found_orders = Order.query.filter_by(user_id=found_user.id).all()
    if not found_orders:
        return jsonify({"orders": order_list})

    for order in found_orders:
        found_status = Status.query.filter_by(id=order.status_id).first()
        status = found_status.status

        order_dict = {"order_id": order.id, "status": status, "vare": order.product, "order_date": order.date_ordered}
        order_list.append(order_dict)
    
    return jsonify({"orders": order_list})

@app.route("/api/order/delete", methods=["POST"])
def delete_order():
    response = request.get_json()
    order_id = response["order_id"]

    found_order = Order.query.filter_by(id=order_id).first()
    if not found_order:
        to_return = {"order_deleted": False}
        print("Order not found")
    else:
        db.session.delete(found_order)
        db.session.commit()
        to_return= {"order_deleted": True}
        print("Order deleted")

    return jsonify(to_return)

@app.route("/api/robot/order/get", methods=["POST"])
def send_data_tp_robot():
    response = request.get_json()

    to_return = "hello"
    return to_return

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

if __name__ == '__main__':
    database_init()
    app.run(debug=True)
