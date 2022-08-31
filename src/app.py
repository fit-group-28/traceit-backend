from flask import Flask
import endpoints.hello_world

app = Flask(__name__)


@app.route("/hello")
def hello_world():
    return endpoints.hello_world.hello_world()
