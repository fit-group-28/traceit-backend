from flask import Flask
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import copy

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
