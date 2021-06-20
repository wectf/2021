import os
import uuid
from typing import Optional
from flask import Flask, render_template, request, redirect, make_response
from peewee import SqliteDatabase, Model, CharField, AutoField, IntegerField, TextField, BooleanField, IntegrityError

app = Flask(__name__)

db = SqliteDatabase("core.db")


class User(Model):
    id = AutoField()
    username = CharField(unique=True)
    password = CharField()
    token = CharField()

    class Meta:
        database = db


class Link(Model):
    id = AutoField()
    user_id = IntegerField()
    link = CharField()
    description = TextField()
    pin = BooleanField(default=False)

    class Meta:
        database = db


@db.connection_context()
def initialize():
    db.create_tables([User, Link])
    try:
        User.create(username=os.getenv("TOKEN"), password=os.getenv("TOKEN"), token=os.getenv("TOKEN"))
        Link.create(user_id=1, link=os.getenv("FLAG_URL"), description="Flag", pin=False)
    except:
        pass


initialize()


def token_to_user_id() -> Optional[int]:
    token = request.cookies.get("token")
    result = User.select().where(User.token == token)
    if len(result) == 0:
        return -1
    return result[0].id


@app.route('/')
def index():
    user_id = token_to_user_id()
    if user_id == -1:
        return redirect("/register")

    keyword = request.args.get("keyword")
    pinned_links = Link.select().where((Link.user_id == user_id) & (Link.pin == True)).limit(10)
    if keyword:
        links = Link.select().where(
            (Link.link.contains(keyword)) & (Link.user_id == token_to_user_id())).limit(10)
    else:
        links = Link.select().where(Link.user_id == user_id).limit(10)
    return render_template("home.html",
                           num_links=len(links), links=links,
                           num_pinned_links=len(pinned_links), pinned_links=pinned_links,
                           keyword=keyword if keyword else "")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username, password = request.form["username"], request.form["password"]
        if len(username) < 10 or len(password) < 10:
            return "Choose a longer password / username"
        token = str(uuid.uuid4())
        try:
            User.create(username=username, password=password, token=token)
        except IntegrityError as e:
            return "Username taken"
        resp = make_response(redirect("/"))
        resp.set_cookie("token", token)
        return resp
    else:
        return render_template("register.html")


@app.route('/add', methods=["POST"])
def add():
    link, description = request.form["link"], request.form["description"]
    Link.create(link=link, description=description, user_id=token_to_user_id())
    return redirect("/")


@app.route('/pin', methods=["POST"])
def pin():
    link = request.form["link"]
    Link.update(pin=True).where((Link.link == link) & (Link.user_id == token_to_user_id())).execute()
    return redirect("/")


@app.route('/unpin', methods=["POST"])
def unpin():
    link = request.form["link"]
    Link.update(pin=False).where((Link.link == link) & (Link.user_id == token_to_user_id())).execute()
    return redirect("/")


if __name__ == '__main__':
    app.run()
