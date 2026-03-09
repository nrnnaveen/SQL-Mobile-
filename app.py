from flask import Flask,render_template,request,redirect,session,send_file
from db import run_query,list_tables,get_table,insert_row,delete_row,export_csv
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route("/",methods=["GET","POST"])
def login():

    if request.method=="POST":

        u=request.form["username"]
        p=request.form["password"]

        if u=="admin" and p=="admin":

            session["user"]=u
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    tables=list_tables()

    return render_template("dashboard.html",tables=tables)


@app.route("/query",methods=["GET","POST"])
def query():

    columns=[]
    data=[]

    if request.method=="POST":

        sql=request.form["query"]

        columns,data=run_query(sql)

    return render_template("query.html",columns=columns,data=data)


@app.route("/tables")
def tables():

    tables=list_tables()

    return render_template("tables.html",tables=tables)


@app.route("/table/<name>")
def table_view(name):

    columns,data=get_table(name)

    return render_template(
        "table_view.html",
        table=name,
        columns=columns,
        data=data
    )


@app.route("/insert/<table>",methods=["POST"])
def insert(table):

    insert_row(table,request.form)

    return redirect(f"/table/{table}")


@app.route("/delete/<table>/<rowid>")
def delete(table,rowid):

    delete_row(table,rowid)

    return redirect(f"/table/{table}")


@app.route("/export/<table>")
def export(table):

    file=export_csv(table)

    return send_file(file,as_attachment=True)


if __name__=="__main__":
    app.run(debug=True)
