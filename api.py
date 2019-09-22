from flask import Flask, escape, request
from velger.py import finn_spill

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'
