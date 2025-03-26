import flask
import random
import requests
import string
# mail za chatGPT random acc hohelo4089@intady.com



app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def loginOrRegister():
    return render_template("login.html")



app.run(debug = True)