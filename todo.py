from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import json
import mysql.connector


# read the json file
with open("2-To do App with Flask\db.json") as f:
    config_data = json.load(f)

# connect to the database server
app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+mysqlconnector://{config_data['user']}:{config_data['password']}@{config_data['host']}:{config_data['port']}/{config_data['database']}"
db = SQLAlchemy(app)


# create a class for the table
class TodoModel(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def index():
    todos = TodoModel.query.all()
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = TodoModel(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for("index"))


# delete a todo
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = TodoModel.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("index"))


# complate a todo
@app.route("/complate/<int:todo_id>")
def complate(todo_id):
    todo = TodoModel.query.get(todo_id)
    if todo:
        todo.complete = not todo.complete
        db.session.commit()
    return redirect(url_for("index"))


def update(todo_id):
    todo = TodoModel.query.get(todo_id)
    if todo:
        todo.complete = not todo.complete
        db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
