from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return redirect("/journal")

@app.route("/journal")
def journal():
    return render_template("journal.html")
