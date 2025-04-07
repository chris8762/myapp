from flask import Flask, render_template, jsonify, request
import random
import requests


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


@app.route("/getAi")
def getAi():
    return "x"


@app.route("/ai")
def ai():
    return render_template("ai_pomocnik.html")



@app.route("/getZdravi")
def getZdravi():
    proteini = request.args.get("proteini")
    mascobe = request.args.get("mascobe")
    kalorije = request.args.get("kalorije")

    if proteini == "":
        proteini = 0

    if mascobe == "":
        mascobe = 0

    if kalorije == "":
        kalorije = 800


    #print(proteini,mascobe,kalorije)
    api2 = f"c3903212f7594031bab178a65e5940a1"
    # testni url = f"https://api.spoonacular.com/recipes/complexSearch?query={sestavine}&cuisine={vrsta}&apiKey={api2}"
    url2 = f"https://api.spoonacular.com/recipes/complexSearch?minProtein={proteini}&maxCalories={kalorije}&minFat={mascobe}&apiKey={api2}"
    call = requests.get(url2).json()
    
    #ime = call["results"][0]["title"]
    #slika = call["results"][0]["image"]
    id = call["results"][0]["id"]
    #print(ime, slika, id)

    #kako dobit recept preko ID-jev
    recept_url = f"https://api.spoonacular.com/recipes/{id}/information?apiKey={api2}"
    recept = requests.get(recept_url).json()
    print(recept)
    
    
    
    
    return "x"


@app.route("/zdravi")
def zdravi():
    return render_template("zdravi_obrok.html")



app.run(debug = True)