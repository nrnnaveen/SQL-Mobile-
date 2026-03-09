from flask import Flask, render_template, request, redirect, session, send_file
from db import run_query, list_tables, export_csv
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin":
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    tables = list_tables()

    return render_template("dashboard.html", tables=tables)


@app.route("/query", methods=["GET", "POST"])
def query():

    columns = []
    data = []

    if request.method == "POST":

        sql = request.form["query"]

        columns, data = run_query(sql)

    return render_template(
        "query.html",
        columns=columns,
        data=data
    )


@app.route("/tables")
def tables():

    tables = list_tables()

    return render_template("tables.html", tables=tables)


@app.route("/export/<table>")
def export(table):

    file = export_csv(table)

    return send_file(file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
