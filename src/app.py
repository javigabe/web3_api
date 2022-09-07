from flask import Flask
import Blockchains

app = Flask(__name__)

@app.route("/userInfo/<address>")
def hello_world(address):
    return "<p>Hello, World!</p>"