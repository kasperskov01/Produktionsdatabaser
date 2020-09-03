from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

def database_init():
    db.create_all()

class Bruger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brugernavn = db.Column(db.String(30), nullable=False)
    # adgangskode = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "<bruger_id %r" % self.id


@app.route('/api/', methods=["POST"])
def main_interface():
    response = request.get_json()
    ny_bruger = Bruger(brugernavn=response["message"])
    print(ny_bruger.brugernavn)

    try:
        db.session.add(ny_bruger)
        db.session.commit
        return redirect("/")
    except:
        return "Der skete en fejl da du prøvede at oprette en bruger"

    return jsonify(response)


# @app.route('/api/user/login?username&password/')
# def login():
#     response = request.get_json()
#     print(response["username"])
#     print(response["password"])

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

if __name__ == '__main__':
    app.run(debug=True)
