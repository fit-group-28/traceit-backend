from endpoints.user_regist import endpoint_register
from flask import Flask
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from endpoints.hello_world import endpoint_hello_world
from endpoints.order import endpoint_order_get
from endpoints.user_details import endpoint_user_details
from endpoints.login import endpoint_login
from userjwt import Jwt


app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = "fit3162traceit"
jwt = JWTManager(app)


# ENDPOINTS
@app.route("/account/login", methods=["POST"])
def login():
    return endpoint_login(request).response_tuple()


@app.route("/account/register", methods=["POST"])
def register():
    return endpoint_register(request).response_tuple()


@app.route("/hello", methods=["GET"])
@jwt_required(optional=True)
def hello_world():
    user_jwt = get_user_jwt()
    return endpoint_hello_world(user_jwt).response_tuple()


@app.route("/user/details", methods=["GET"])
@jwt_required()
def user_details():
    user_jwt = get_user_jwt()
    return endpoint_user_details(user_jwt).response_tuple()


@app.route("/order", methods=["GET", "POST", "PATCH"])
@jwt_required()
def order():
    user_jwt = get_user_jwt()
    return endpoint_order_get(user_jwt).response_tuple()


# UTILS
def get_user_jwt() -> Jwt | None:
    """
    Get the user's JWT.

    Returns:
        The user's JWT if it exists, None otherwise.
    """
    try:
        return (
            Jwt.from_dict(user_identity)
            if (user_identity := get_jwt_identity())
            else None
        )
    except:
        return None


if __name__ == "__main__":
    app.run(debug=True, port=3000)
