from flask import Flask
from endpoints.hello_world import endpoint_hello_world

app = Flask(__name__)


@app.route("/hello")
def hello_world():
    return endpoint_hello_world()


if __name__ == "__main__":
    app.run(debug=True)
