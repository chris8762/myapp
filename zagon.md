# 🍲 Spletna aplikacija Gurmanski svet

Išči recepte in uporabi priročne funkcije.

---

## 📋 Predpogoji

Prepričajte se, da imate na svojem sistemu nameščeno:

- Python 3.8 ali novejši  
- pip (Python package manager)

---

## 🚀 Navodila za zagon

### 1. Prenos projekta

Prenesite ali klonirajte projekt v svojo mapo.

### 2. Namestitev odvisnosti

Namestite potrebne Python pakete:

```
from flask import Flask, render_template, jsonify, request, redirect, session
import random
import requests
import sqlite3
import bcrypt
```
### 3. Zagon aplikacije

**Razvojni način (testiranje):**

```bash
python main.py
```

Zaženite aplikacijo:

```bash
gunicorn -w 4 -b 0.0.0.0:5001 main:app
```

---

## 🌐 Dostop do aplikacije

- Lokalni dostop: [http://localhost:5001](http://localhost:5001)  
- Mrežni dostop: `http://<IP_naslov_računalnika>:5001`

---

## 🔑 Privzeti dostopi

**Admin račun:**

- Uporabniško ime: `admin`  
- Geslo: `admin`

**Nova registracija:**

- Obiščite `/register` in ustvarite nov račun.  
- Po registraciji se prijavite z ustvarjenimi podatki.

---

## 📁 Struktura projekta

```
ReceptApp/
├── main.py                  # Glavna Flask aplikacija
├── users.db                 # SQLite baza za uporabnike
├── recepti.db               # SQLite baza za recepte
├── templates/               # HTML predloge
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── uporabniki.html
│   ├── recepti.html
│   ├── dodaj_recept.html
│   ├── uredi_recept.html
│   └── recept_detail.html
├── static/
│   └── style.css            # CSS stil
└── README.md
```

---

## 🌟 Glavne funkcionalnosti

### Uporabniške funkcionalnosti:
✅ Registracija in prijava  
✅ Dodajanje, urejanje in brisanje receptov  
✅ Iskanje receptov po ključnih besedah  
✅ Ogled receptov drugih uporabnikov  

### Admin funkcionalnosti:
✅ Pregled vseh uporabnikov  
✅ Brisanje uporabnikov  
✅ Dostop do vseh receptov  

---

## 🔒 Varnost

- Gesla so varno shranjena z `bcrypt` hashiranjem  
- Uporabniki imajo ločene pravice (admin/navadni)  

---

## 🛠️ Razreševanje težav

**Aplikacija se ne zažene:**  
- Preverite Python verzijo: `python --version`  
- Preverite pakete: `pip list`

**Port 5001 je zaseden:**  
- Spremenite port v `main.py` (npr. na 5002)

**Napaka z bazo:**  
- Izbrišite `.db` datoteko za ponovni zagon prazne baze

---

## 📞 Podpora

**Avtor:** Jaša Toporš 
**Email:** jasa.topors@gmail.com  
**GitHub:** [https://github.com/chris8762/myapp]

---

🚀 Gurmanski svet!  
