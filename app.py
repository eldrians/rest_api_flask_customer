from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def welcome():
    return "Axel Eldrian Hadiwibowo"


from controller import *
