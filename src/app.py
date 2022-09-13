from flask import Flask
from Blockchains import get_all_liquidity_by_user

app = Flask(__name__)

@app.before_first_request
def before_first_request():
    #run_config()
    pass


@app.route("/userInfo/<address>")
def get_liquidity_by_user(address):
    return get_all_liquidity_by_user(address)
