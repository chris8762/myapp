from flask import Flask, render_template, jsonify, request
import random
import requests
import string



app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def loginOrRegister():
    return render_template("login.html")

#glavne funkcije
@app.route("/randomRecipe")
def randomRecipe():
    return render_template("randomRecipe.html")


#testiram commit




app.run(debug = True)