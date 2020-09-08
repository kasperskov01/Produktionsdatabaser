from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# db = SQLAlchemy(app)

# def database_init():
#     db.create_all()

# class users(db.Model):

#     id = db.Column(db.Integer, primary_key=True)
#     brugernavn = db.Column(db.String(30), nullable=False)
#     adgangskode = db.Column(db.String(20), nullable=False)

#     def __init__(self, brugernavn, adgangskode):
#         self.brugernavn = brugernavn
#         self.adgangskode = adgangskode


#     def __repr__(self):
#         return "<bruger_id %r" % self.id

# @app.route('/api/', methods=["POST"])
# def main_interface():
#     response = request.get_json()
#     ny_bruger = users(brugernavn=response["message"])
#     print(ny_bruger.brugernavn)


@app.route('/api/login', methods=["POST"])
# @cross_origin()
def login():
    response = request.get_json()
    username = response["username"]
    password = response["password"]

    found_user = users.query.filter_by(username=username).first()
    if found_user:
        pass
    else:
        new_user = users(response["username"],response["password"])
        db.session.add(new_user)
        db.session.commit()

    print(response["username"])
    print(response["password"])
    print(jsonify(response))

    return jsonify(response)

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
