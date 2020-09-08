from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

def database_init():
    db.create_all()

class users(db.Model):

    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password, user_type):
        self.username = username
        self.password = password
        self.user_type = user_type

    def __repr__(self):
        return "<bruger_id %r" % self._id


@app.route('/api/user/signup', methods=["POST"])
def opret():
    response = request.get_json()
    username = response["username"]
    password = response["password"]
    user_type = response["user_type"]

    found_user = users.query.filter_by(username=username).first()

    if found_user:
        to_return = {"user_exists": True}
        print("user already created")
    else:
        new_user = users(username, password, user_type)
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
    

    found_user = users.query.filter_by(username=username).first()
    if found_user:
        if password == found_user.password:
            to_return = {"username": username, "logged_in": True, "user_type": found_user.user_type}
            print("logged in")
        else:
            to_return = {"username": username, "logged_in": False, "user_type": found_user.user_type}
            print("password incorrect")
    else:
        print("user not found")
        to_return = {"logged_in": False}
    
    return jsonify(to_return)


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(debug=True)