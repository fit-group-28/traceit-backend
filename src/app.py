from flask import Flask
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from endpoints.hello_world import endpoint_hello_world
from endpoints.login import endpoint_login

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "fit3162traceit"  # Change this!
jwt = JWTManager(app)


@app.route("/hello")
def hello_world():
    return endpoint_hello_world().response_tuple()


@app.route("/login", methods=["POST"])
def login():
    return endpoint_login(request).response_tuple()


if __name__ == "__main__":
    app.run(debug=True)
