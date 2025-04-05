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


#dost za dones prisel sem na limit za API
@app.route("/getRandomRecipe")
def getRandomRecipe():
    sestavine = request.args.get("sestavine")
    vrsta = request.args.get("vrsta")
    url = f"https://api.spoonacular.com/recipes/complexSearch?query={sestavine}&cuisine={vrsta}&apiKey=32be0b921f2a4e7fac0f85279c03b8cb"

    call = requests.get(url).json()
    get_recept = random.choice(call["results"])
    id_recepta = get_recept["id"]

    recept_url = f"https://api.spoonacular.com/recipes/{id_recepta}/information?apiKey=32be0b921f2a4e7fac0f85279c03b8cb"

    recept = requests.get(recept_url).json()

    ing = []
    amount = []
    unit = []
    for ingredient in recept["extendedIngredients"]:
        if "nameClean" in ingredient:
            amount.append(ingredient["original"])


    print(ing,amount )

    return jsonify({"slika": f"<img src={recept["image"]}>",
                    "ime": recept["title"],
                    "ingredients": amount,
                    "navodila": recept["instructions"]})





@app.route("/getHladilnik")
def getHladilnik():
    return "x"


@app.route("/hladilnik")
def hladilnik():
    return render_template("hladilnik.html")

@app.route("/getKalkulator")
def getKalkulator():
    return "x"


@app.route("/kalkulator")
def kalkulator():
    return render_template("kalkulator.html")
#testiram commit

@app.route("/getAi")
def getAi():
    return "x"


@app.route("/ai")
def ai():
    return render_template("ai_pomocnik.html")
#testiram commit





app.run(debug = True)