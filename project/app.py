import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime


from helpers import login_required, apology

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///snapbook.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    if request.method == "GET":
        albums = db.execute("SELECT * FROM AlbumUsers WHERE user_id = ?", session["user_id"])
        albumsUser = []
        administradores = []
        for index, album in enumerate(albums):
            albumDb = db.execute("SELECT * FROM album WHERE id = ?", album["album_id"])
            participantes = db.execute("SELECT users.name FROM users INNER JOIN AlbumUsers ON AlbumUsers.user_id = users.id WHERE AlbumUsers.album_id = ?", album["album_id"])


            administrador = db.execute("SELECT name FROM users WHERE id = ?", albumDb[0]['adm'])
            albumsUser.append({'name': albumDb[0]['name'], 'administrador' : administrador[0]['name'], 'participantes': participantes})



        return render_template("index.html", albumsUser = albumsUser)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        if not request.form.get("username"):
            print("must provide a username")
            return 0

        elif not request.form.get("password"):
            print("must provide a password")
            return 0


        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))


        print(request.form.get("password"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            print("invalid user or/and password")
            return 0

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        number_digits = 0
        name = request.form.get("name")
        lastName = request.form.get("lastName")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        for i in password:
            if i.isdigit():
                number_digits += 1


        if not name:
            print("name is blank")

        elif password != confirmation or password == "":
            print("passwords are not the same")
            print("Password is blank or they do not match")
        # elif len(password) < 8:
        #     return apology("Password must have at least 8 characters", 200)
        # elif number_of_digits < 3:
        #     return apology("Password must have at least 3 digits", 200)

        else:
            users = db.execute("SELECT username FROM users WHERE username = ?", username)

            if len(users) == 0:
                db.execute("INSERT INTO users (name, lastName, username, hash) VALUES(?, ?, ?, ?)", name, lastName, username, generate_password_hash(password))
            else:
                print("Username already exist")


        return redirect("/login")




@app.route("/album", methods=["GET"])
@login_required
def album():
    pass

@app.route("/createAlbum", methods=["GET", "POST"])
@login_required
def createAlbum():
    if request.method == "GET":
        return render_template("createAlbum.html")
    else:
        name = request.form.get("name")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if password != confirmation:
            print("the passwords do not match")
            # aqui eu tenho que renderizar uma tela ou um pop-up falando que as senhas nao batem
            return 0

        albums = db.execute('SELECT name FROM album WHERE name = ?', name)

        if len(albums) != 0:
            print("the album name already exist")
            # aqui eu tenho que renderizar uma tela falando que o nome do album ja existe
            return 0

        db.execute("INSERT INTO album (name, adm, hash) VALUES(?, ?, ?)", name, session["user_id"], generate_password_hash(password))
        album_id = db.execute("SELECT id FROM album WHERE name = ?", name)
        album_id = album_id[0]["id"]
        db.execute("INSERT INTO AlbumUsers (album_id, user_id) VALUES (?, ?)", album_id, session["user_id"])


        return redirect("/")








@app.route("/accessAlbum", methods=["GET", "POST"])
@login_required
def acessAlbum():
    if request.method == "GET":
        # albums = db.execute("SELECT * FROM AlbumUsers WHERE user_id = ?", session["user_id"])
        # albumsUser = []
        # administradores = []
        # for index, album in enumerate(albums):
        #     albumDb = db.execute("SELECT * FROM album WHERE id = ?", album["album_id"])
        #     participantes = db.execute("SELECT users.name FROM users INNER JOIN AlbumUsers ON AlbumUsers.user_id = users.id WHERE AlbumUsers.album_id = ?", album["album_id"])


        #     administrador = db.execute("SELECT name FROM users WHERE id = ?", albumDb[0]['adm'])
        #     albumsUser.append({'name': albumDb[0]['name'], 'administrador' : administrador[0]['name'], 'participantes': participantes})


        return render_template("accessAlbum.html")
    elif request.method == "POST":
        albumsSearch = []
        name = request.form.get("name")
        albums = db.execute("SELECT * FROM album WHERE name LIKE ?", ('%' + name + '%',))
        for album in albums:
            adm = db.execute("SELECT name FROM users WHERE id = ?", album['adm'])
            albumsSearch.append({'name': album['name'], 'adm': adm[0]['name']})

        


        return render_template("accessAlbum.html", albumsUser = albumsSearch)



@app.route("/unlockAlbum", methods=["GET", "POST"])
@login_required

def unlockAlbum():
    if request.method == "POST":
        name = request.form.get("cardName")
        password = request.form.get("senha")
        album = db.execute("SELECT * FROM album WHERE name = ?", (name))
        if check_password_hash(album[0]["hash"], password) == True:
            id_album = album[0]['id']
            participa = db.execute("SELECT * FROM AlbumUsers WHERE album_id = ? AND user_id = ?", id_album, session["user_id"])
            if(len(participa) > 0):
                return apology("You already is a member of this album")
            else:
                db.execute("INSERT INTO AlbumUsers (album_id, user_id) VALUES (?, ?)", id_album, session["user_id"])
                return render_template("accessAlbum.html")

        else:
            print('chegou aqui')
            return apology("The password is incorrect")


@app.route("/renderAlbum", methods=["GET", "POST"])
@login_required

def renderAlbum():
    if request.method == "POST":
        print("chegou aqui em renderAlbum")
        name = request.form.get("cardName")

        return render_template("album.html", albumName = name)

@app.route("/uploadImage", methods = ["GET"])
@login_required

def uploadImage():
    if request.method == "POST":
        print("chegou aqui em upload images")





