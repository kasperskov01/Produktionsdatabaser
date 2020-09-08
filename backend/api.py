from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

def database_init():
    db.create_all()

class users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


    def __repr__(self):
        return "<bruger_id %r" % self.id

# @app.route('/api/', methods=["POST"])
# def main_interface():
#     response = request.get_json()
#     ny_bruger = users(username=response["message"])
#     print(ny_bruger.username)


@app.route('/api/user/login', methods=["POST"])
# @cross_origin()
def login():
    response = request.get_json()
    username = response["username"]
    password = response["password"]

    # found_user = users.query.filter_by(username=username).first()
    # if found_user:
    #     pass
    # else:
    #     new_user = users(response["username"],response["password"])
    #     db.session.add(new_user)
    #     db.session.commit()
    
    to_return = {"username": response["username"], "logged_in": True}
    print(to_return)
    return jsonify(to_return)

# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5500')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   response.headers.add('Access-Control-Allow-Credentials', 'true')
#   return response
    

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

if __name__ == '__main__':
    app.run(debug=True)