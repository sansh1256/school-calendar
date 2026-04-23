from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY, text TEXT, type TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS homework
                 (id INTEGER PRIMARY KEY, text TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, text TEXT)""")

    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if request.method == "POST":
        text = request.form["text"]
        type_ = request.form["type"]

        c.execute("INSERT INTO events (text, type) VALUES (?, ?)", (text, type_))
        conn.commit()

    c.execute("SELECT * FROM events")
    events = c.fetchall()

    conn.close()
    return render_template("index.html", events=events)


@app.route("/homework", methods=["GET", "POST"])
def homework():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if request.method == "POST":
        text = request.form["text"]
        c.execute("INSERT INTO homework (text) VALUES (?)", (text,))
        conn.commit()

    c.execute("SELECT * FROM homework")
    data = c.fetchall()

    conn.close()
    return render_template("homework.html", data=data)


@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if request.method == "POST":
        text = request.form["text"]
        c.execute("INSERT INTO tasks (text) VALUES (?)", (text,))
        conn.commit()

    c.execute("SELECT * FROM tasks")
    data = c.fetchall()

    conn.close()
    return render_template("tasks.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
