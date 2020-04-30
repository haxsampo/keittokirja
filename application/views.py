from flask import render_template, flash
from application import app

@app.route("/")
def index():
    return render_template("index.html")