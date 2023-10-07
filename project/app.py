import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date


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
            # participantes = db.execute("SELECT users.name FROM users INNER JOIN AlbumUsers ON AlbumUsers.user_id = users.id WHERE AlbumUsers.album_id = ?", album["album_id"])


            administrador = db.execute("SELECT name FROM users WHERE id = ?", albumDb[0]['adm'])
            albumsUser.append({'name': albumDb[0]['name'], 'administrador' : administrador[0]['name'],  'cover': albumDb[0]['cover']})



        return render_template("index.html", albumsUser = albumsUser)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        if not request.form.get("username"):
            return apology("Must provide a username")
            return 0

        elif not request.form.get("password"):
            return apology("Must return a password")
            return 0


        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))


        print(request.form.get("password"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid user or/and password")
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
            return apology("Name is blank")

        elif password != confirmation or password == "":
            return apology("Password is blank or they do not match")

        # elif len(password) < 8:
        #     return apology("Password must have at least 8 characters", 200)
        # elif number_of_digits < 3:
        #     return apology("Password must have at least 3 digits", 200)

        else:
            users = db.execute("SELECT username FROM users WHERE username = ?", username)

            if len(users) == 0:
                db.execute("INSERT INTO users (name, lastName, username, hash) VALUES(?, ?, ?, ?)", name, lastName, username, generate_password_hash(password))
            else:
                return apology("Username already exist")



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
        coverImage = request.form.get("coverImage")

        if password != confirmation:
            return apology("The passwords do not match")
            # aqui eu tenho que renderizar uma tela ou um pop-up falando que as senhas nao batem
            return 0

        albums = db.execute('SELECT name FROM album WHERE name = ?', name)

        if len(albums) != 0:
            return apology("The album name already exist")
            # aqui eu tenho que renderizar uma tela falando que o nome do album ja existe
            return 0

        db.execute("INSERT INTO album (name, adm, hash, cover) VALUES(?, ?, ?, ?)", name, session["user_id"], generate_password_hash(password), coverImage)
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
        userAlbums = db.execute("SELECT album_id FROM AlbumUsers WHERE user_id = ?", session["user_id"])

        print(userAlbums)
        albumList = [x['album_id'] for x in userAlbums]

        print(albumList)
        albums = db.execute("SELECT * FROM album WHERE name LIKE ?", ('%' + name + '%',))
        for album in albums:
            print(album)
            adm = db.execute("SELECT name FROM users WHERE id = ?", album['adm'])
            albumsSearch.append({'name': album['name'], 'adm': adm[0]['name'], 'userInAlbum' : (album['id'] not in albumList), 'cover': album['cover']})


        

        return render_template("accessAlbum.html", albumsUser = albumsSearch)



@app.route("/unlockAlbum", methods=["GET", "POST"])
@login_required

def unlockAlbum():
    if request.method == "POST":
        name = request.form.get("cardName")
        password = request.form.get("senha")
        album = db.execute("SELECT * FROM album WHERE name = ?", (name))
        print(album)
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


def get_images_and_album_name(album_id):
    images = db.execute("SELECT * FROM images WHERE album_id = ?", album_id)

    for image in images:
        userName = db.execute("SELECT name, lastName FROM users WHERE id = ?", image['user_id'])
        image['authorName'] = userName[0]['name'] + " " + userName[0]['lastName']

    return images



def statusAdm(album_id):
    adm = db.execute("SELECT adm FROM album WHERE id = ?", album_id)

    return (adm[0]['adm'] == session["user_id"])


@app.route("/renderAlbum", methods=["GET", "POST"])
@login_required

def renderAlbum():
    if request.method == "POST":
        name = request.form.get("cardName")
        album_id = db.execute("SELECT id FROM album WHERE name = ?", name)


        status_adm = statusAdm(album_id[0]['id'])




        images = get_images_and_album_name(album_id[0]['id'])


        return render_template("album.html", albumName = name, images = images, statusAdm = status_adm)



@app.route("/uploadImage", methods = ["GET", "POST"])
@login_required

def uploadImage():
    if request.method == "POST":
        name = request.form.get("albumName")
        album_id = db.execute("SELECT id FROM album WHERE name = ?", name)
        description = request.form.get("description")
        url = request.form.get("url_image")



        #TODO fazer verificação se o usuario pode postar algo no site
        db.execute("INSERT INTO images (album_id, user_id, description, url, post_date) VALUES(?, ?, ?, ?, ?);", album_id[0]['id'], session["user_id"], description, url, date.today())


        images = get_images_and_album_name(album_id[0]['id'])

        status_adm = statusAdm(album_id[0]['id'])




        return render_template("album.html", albumName=name, images=images, statusAdm = status_adm)




@app.route("/updateImage", methods = ["GET", "POST"])
@login_required

def updateImage():
    if request.method == "POST":
        description = request.form.get("description")
        url = request.form.get("url_image")
        id = request.form.get("id")



        db.execute("UPDATE images SET description = ?, url = ? WHERE id = ?", description, url, id)

        album_id = db.execute("SELECT album_id FROM images WHERE id = ?", id)

        name = db.execute("SELECT name FROM album WHERE id = ?", album_id[0]['album_id'])


        images = get_images_and_album_name(album_id[0]['album_id'])

        status_adm = statusAdm(album_id[0]['album_id'])

        return render_template("album.html", albumName=name[0]['name'], images=images, statusAdm = status_adm)


        #fazer verificação se o usuario poder editar algo no site



@app.route("/deleteImage", methods = ["GET", "POST"])
@login_required

def deleteImage():
    if request.method == "POST":
        id = request.form.get("id")

        try:
            id = int(id)
        except ValueError:
            return "ID inválido."


        album_id = db.execute("SELECT album_id FROM images WHERE id = ?", id)


        db.execute("DELETE FROM images WHERE id = ?", id)

        name = db.execute("SELECT name FROM album WHERE id = ?", album_id[0]['album_id'])


        images = get_images_and_album_name(album_id[0]['album_id'])

        status_adm = statusAdm(album_id[0]['album_id'])


        return render_template("album.html", albumName=name[0]['name'], images=images, statusAdm = status_adm)






