# za pregled po bazi v terminalu: sqlite3 users.db ---> potem pa SELECT * FROM users;

from flask import Flask, render_template, jsonify, request, redirect, session
import random
import requests
import sqlite3
import bcrypt



conn = sqlite3.connect('users.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    mail TEXT,
    geslo TEXT
)''')

conn.commit()
conn.close()


conn = sqlite3.connect('recepti.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS recepti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    naslov TEXT,
    slika TEXT,
    sestavine TEXT,
    navodila TEXT,
    tezavnost TEXT,
    cas_priprave INTEGER,
    osebe INTEGER
)''')

conn.commit()
conn.close()

app = Flask(__name__)
app.secret_key = "1234"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        mail = request.form.get("mail")
        geslo = request.form.get("geslo")

        geslo_utf = geslo.encode('utf-8')
        hash_geslo = bcrypt.hashpw(geslo_utf, bcrypt.gensalt()).decode('utf-8')


        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("SELECT username FROM users WHERE username = ?", (username,))
        if c.fetchone():
            conn.close()
            return jsonify({"message": "Uporabnisko ime ze obstaja", "povezava": "/register"})

        c.execute("SELECT mail FROM users WHERE mail = ?", (mail,))
        if c.fetchone():
            conn.close()
            return jsonify({"message": "Registracija uspesna!", "povezava": "/register"})

        c.execute("INSERT INTO users (username, mail, geslo) VALUES (?, ?, ?)", (username, mail, hash_geslo))
        conn.commit()
        conn.close()
        return jsonify({"message": "Registracija uspesna!", "povezava": "/login"})
        
    
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        geslo = request.form.get("geslo")

        geslo_utf = geslo.encode('utf-8')

        baza = sqlite3.connect('users.db')
        c = baza.cursor()
        c.execute("SELECT username, geslo FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        baza.close()

        if user is not None:
            db_username = user[0]
            db_hash = user[1] 

            if bcrypt.checkpw(geslo_utf, db_hash.encode('utf-8')):  

                session["username"] = db_username
                return jsonify({"message": "Prijava uspešna!", "povezava": "/"})
            else:
                return jsonify({"message": "Napačno geslo.", "povezava": "/login"})
        else:
            return jsonify({"message": "Napačno uporabniško ime ali geslo.", "povezava": "/login"})



    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        username = session["username"]
        if  username == "admin":
            return render_template("dashboard.html", username=username)
        else:
            return render_template("index.html", username=username)
        
    else:
        return redirect("/login")


@app.route("/uporabniki")
def uporabniki():
    if "username" in session:
        username = session["username"]
        if  username == "admin":
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("SELECT id, username, mail FROM users")
            users = c.fetchall()
            conn.close()

            return render_template("uporabniki.html", users=users)
        
        else:
            return render_template("index.html", username=username)

    else:
        return redirect("/login")

@app.route("/recepti")
def recepti():
    if "username" in session:
        username = session["username"]
        if  username == "admin":
            conn = sqlite3.connect('recepti.db')
            c = conn.cursor()
            c.execute("SELECT id, naslov, sestavine, navodila FROM recepti")
            recept = c.fetchall()
            conn.close()
            return render_template("recepti.html", recepti=recept)
        
        else:
            return render_template("index.html", username=username)

    else:
        return redirect("/login")


@app.route("/izbrisi/<id>", methods=["POST"])
def izbrisi(id):
    if "username" in session:
        username = session["username"]
        if username == "admin":
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE id = ?", (id,))
            conn.commit()
            conn.close()
            return redirect("/uporabniki")

    else:
        return render_template("index.html", username=username)


@app.route("/izbrisi_recept/<int:id>", methods=["POST"])
def izbrisi_recept(id):
    if "username" in session and session["username"] == "admin":
        with sqlite3.connect('recepti.db') as conn:
            c = conn.cursor()
            c.execute("DELETE FROM recepti WHERE id = ?", (id,))
            conn.commit()
        return redirect("/recepti")  
    else:
        return redirect("/login")  

#---------------druge strani-------------------
#------------------------------------------------------
#------------------------------------------------------
@app.route("/")
def index():

    if "username" in session:
        username = session["username"]
        if  username == "admin":
            return render_template("admin_index.html", username=username)
        else:
            return render_template("index.html", username=username)
    
    else:
        return render_template("index.html")


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


    #print(ing,amount )

    return jsonify({"slika": f"<img src={recept["image"]}>",
                    "ime": recept["title"],
                    "ingredients": amount,
                    "navodila": recept["instructions"]})



@app.route("/getHladilnik")
def getHladilnik():
    sestavina1 = request.args.get("sestavina1")
    sestavina2 = request.args.get("sestavina2")
    sestavina3 = request.args.get("sestavina3")
    sestavina4= request.args.get("sestavina4")

    sestavine = sestavina1 + "," + sestavina2 + "," + sestavina3 + "," + sestavina4
    #print(sestavine)
    url = f"https://api.spoonacular.com/recipes/complexSearch?query={sestavine}&apiKey=32be0b921f2a4e7fac0f85279c03b8cb"

    call = requests.get(url).json()

    #print(call)

    if call["totalResults"] == 0:
        return jsonify({"message": "Recept s takimi sestavinami ne obstaja."})
    
    else:
        id = call["results"][0]["id"]
        #print(id)
        url = f"https://api.spoonacular.com/recipes/{id}/information?apiKey=6fea24f6376a45eb9033908b8bbc7579"

        call_recept = requests.get(url).json()

        #print(call_recept)

        amount = []
        for ingredient in call_recept["extendedIngredients"]:
            if "nameClean" in ingredient:
                amount.append(ingredient["original"])


        return jsonify({"slika": f"<img src={call_recept["image"]}>",
                        "ime": call_recept["title"],
                        "sestavine": amount,
                        "navodila": call_recept["instructions"]})

    
@app.route("/hladilnik")
def hladilnik():
    return render_template("hladilnik.html")



@app.route("/getKalkulator")
def getKalkulator():
    api = "c2349e0991734b2b9b61908591c4aaab"
    kolicina1 = request.args.get("kolicina1")
    kolicina2 = request.args.get("kolicina2")
    kolicina3 = request.args.get("kolicina3")
    kolicina4 = request.args.get("kolicina4")
    kolicina5 = request.args.get("kolicina5")
    kolicina6 = request.args.get("kolicina6")

    stevilo = request.args.get("stevilo")


    sez_kolicin = [kolicina1, kolicina2, kolicina3, kolicina4, kolicina5, kolicina6]
    pretvorjene = []

    for sestavina in sez_kolicin:
        if sestavina == "":
            sestavina = 0
        else:
            pretvorjene.append(round(int(sestavina) / int(stevilo)))


    #print(pretvorjene)

    return {"pretvorjene": pretvorjene}


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

    sez_recipes = []

    for recipe in call["results"]:
        recipe_info = {
            "id": recipe["id"],
            "title": recipe["title"],
            "calories": None,
            "protein": None
        }

        for nutrient in recipe["nutrition"]["nutrients"]:
            if nutrient["name"] == "Calories":
                recipe_info["calories"] = nutrient["amount"]
            if nutrient["name"] == "Protein":
                recipe_info["protein"] = nutrient["amount"]

        sez_recipes.append(recipe_info)

    #(sez_recipes)

    return jsonify({'recipes': sez_recipes})

@app.route("/zdravi")
def zdravi():
    return render_template("zdravi_obrok.html")



@app.route("/getTecaji")
def getTecaji():
    return "x"

@app.route("/tecaji")
def tecaji():
    return render_template("kuharski_tecaji.html")



@app.route("/getDodajRecept")
def getDodajRecept():

    naslov = request.args.get("naslov")
    sestavine = request.args.get("sestavine")
    navodila = request.args.get("navodila")
    tezavnost = request.args.get("tezavnost")
    cas_priprave = request.args.get("casPriprave")
    osebe = request.args.get("osebe")
    
    #print(f"Recept: {naslov}, {sestavine}, {navodila}, {tezavnost}, {cas_priprave}, {osebe}")

    conn = sqlite3.connect('recepti.db') 
    c = conn.cursor()
    
    c.execute('''INSERT INTO recepti (naslov, sestavine, navodila, tezavnost, cas_priprave, osebe)
                 VALUES ( ?, ?, ?, ?, ?, ?)''', 
              (naslov, sestavine, navodila, tezavnost, cas_priprave, osebe))

    conn.commit()
    conn.close()

    return jsonify({"message": "Recept uspešno oddan v pregled!"})


@app.route("/dodajRecept")
def dodajRecept():
    return render_template("dodaj_recept.html")



@app.route("/getInfo")
def getInfo():

    #api 6fea24f6376a45eb9033908b8bbc7579
    api_key = "6fea24f6376a45eb9033908b8bbc7579" 
    sestavina = request.args.get("sestavina")

    url = f"https://api.spoonacular.com/food/ingredients/search?query={sestavina}&apiKey={api_key}"
    call = requests.get(url).json()

    id_sestavine = call["results"][0]["id"]
    #print(call["results"][0]["id"])

    url_info = f"https://api.spoonacular.com/food/ingredients/{id_sestavine}/information?amount=1&apiKey={api_key}"

    call_info = requests.get(url_info).json()

    sez_info = [
        "Protein",
        "Carbohydrates",
        "Fiber",
        "Fat",
        "Sugar",
        "Calories",
        "Vitamin C",
        "Vitamin A",
        "Vitamin B6",
        "Vitamin B12",
        "Iron",
        "Magnesium",
        "Potassium",
        "Calcium"
    ]

    nutrition = {
        "name": call_info["name"]
    }

    for item in call_info["nutrition"]["nutrients"]:
        if item["name"] in sez_info:
            nutrition[item["name"]] = {
                "amount": item["amount"],
                "unit": item["unit"]
            }

    print(nutrition)
    return jsonify(nutrition)


@app.route("/info")
def info():
    return render_template("info_sestavine.html")



@app.route("/getIdSearch")
def getIdSearch():

    id = request.args.get("id")
    url = f"https://api.spoonacular.com/recipes/{id}/information?apiKey=6fea24f6376a45eb9033908b8bbc7579"

    call = requests.get(url).json()
    #print(call)

    amount = []
    for ingredient in call["extendedIngredients"]:
        if "nameClean" in ingredient:
            amount.append(ingredient["original"])


    #print(ing,amount )

    return jsonify({"slika": f"<img src={call["image"]}>",
                    "ime": call["title"],
                    "ingredients": amount,
                    "navodila": call["instructions"]})


@app.route("/idSearch")
def idSearch():
    return render_template("id_search.html")

@app.route("/pretvori")
def pretvori():
    return render_template("pretvori.html")


@app.route("/getPretvori")
def getPretvori():

    ing = request.args.get("ing")
    amount = request.args.get("amount")
    enota = request.args.get("enota")
    pretvorjena = request.args.get("pretvorjena")
    api_key = "c2349e0991734b2b9b61908591c4aaab"
    url = f"https://api.spoonacular.com/recipes/convert?ingredientName={ing}&sourceAmount={amount}&sourceUnit={enota}&targetUnit={pretvorjena}&apiKey={api_key}"

    call = requests.get(url).json()
    #print(call)

    return call["answer"]


app.run(debug = True)