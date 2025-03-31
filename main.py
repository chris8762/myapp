import flask
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

#testi v browserju

app.run(debug = True)
