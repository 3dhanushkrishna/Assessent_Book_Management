from flask import Flask, request, render_template
import sqlite3 as sql

from werkzeug.utils import redirect

connection = sql.connect("Books.db", check_same_thread=False)

listoftables = connection.execute("SELECT NAME FROM sqlite_master WHERE type='table' AND name= 'Book'").fetchall()

if listoftables != []:
    print("Table Already Exist")
else:
    connection.execute('''CREATE TABLE Book(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME TEXT,
                        AUTHOR TEXT,
                        CATEGORY TEXT,
                        PRICE TEXT,
                        PUBLISHER TEXT
                       )''')

    print("Table Created Successfully")

listoftables2 = connection.execute("SELECT NAME FROM sqlite_master WHERE type='table' AND name= 'User'").fetchall()

if listoftables2 != []:
    print("Table Already Exist")
else:
    connection.execute('''CREATE TABLE User(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME TEXT,
                        ADDRESS TEXT,
                        EMAIL TEXT,
                        PHONE INTEGER,
                        PASS TEXT
                       )''')

    print("Table Created Successfully")
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    global result1, result2, a, b
    if request.method == "POST":
        getEmail = request.form["email"]
        getPass = request.form["pass"]
        result1 = connection.execute("select EMAIL from User")
        result2 = connection.execute("select PASS from User")

        for i in result1:
            print(i[0])
            result1 = i[0]

        for j in result2:
            print(j[0])
            result2 = j[0]
        if getEmail == result1 and getPass == result2:
            return redirect('/login')
        else:
            return render_template("userlogin.html", status=True)


    else:

        return render_template("userlogin.html", status=False)


@app.route('/userreg', methods=['GET', 'POST'])
def User_Register():
    if request.method == "POST":
        getName = request.form["name"]
        getAdd = request.form["add"]
        getnEmail = request.form["email"]
        getPhone = request.form["pno"]
        getnPass = request.form["pass"]
        result1 = connection.execute("select EMAIL from User")
        for i in result1:
            print(i[0])
            a = i[0]
        if getnEmail != result1:
            connection.execute("INSERT INTO USER(NAME, ADDRESS, EMAIL, PHONE, PASS) \
                            VALUES('" + getName + "', '" + getAdd + "', '" + getnEmail + "', " + getPhone + ", '" + getnPass + "')")
            connection.commit()
            print("Inserted Successfully")
            return redirect('/')
        else:
            return render_template("userregister.html", status=True)


    else:

        return render_template("userregister.html", status=False)


@app.route('/logout')
def logout():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def admin_Login():
    if request.method == "POST":
        getUser = request.form["uname"]
        getPass = request.form["pass"]
        if getUser == "admin" and getPass == "9875":
            return redirect('/dash')
        else:
            return render_template("login.html", status=True)
    else:
        return render_template("login.html", status=False)


@app.route('/dash', methods=['GET', 'POST'])
def dashboard():
    if request.method == "POST":
        getName = request.form["name"]
        getAu = request.form["auth"]
        getCat = request.form["cat"]
        getPrice = request.form["price"]
        getPub = request.form["pub"]

        connection.execute("INSERT INTO Book(NAME, AUTHOR, CATEGORY, PRICE, PUBLISHER) \
        VALUES('" + getName + "', '" + getAu + "', '" + getCat + "', '" + getPrice + "', '" + getPub + "')")
        connection.commit()
        print("Inserted Successfully")
        return redirect('/view')
    return render_template("dashboard.html")


@app.route('/view')
def viewall():
    cursor = connection.cursor()
    count = cursor.execute("SELECT * FROM Book")

    result = cursor.fetchall()
    return render_template("view.html", books=result)


@app.route('/search', methods=['GET', 'POST'])
def search():
    cursor = connection.cursor()
    if request.method == "POST":
        getName = request.form["name"]
        count = cursor.execute("SELECT * FROM Book WHERE NAME='" + getName + "'")
        result = cursor.fetchall()
        if result is None:
            print("Book Name Not Exist")
        else:
            return render_template("search.html", search=result, status=True)
    else:
        return render_template("search.html", search=[], status=False)


@app.route('/delete', methods=['GET', 'POST'])
def deletion():
    cursor = connection.cursor()
    if request.method == "POST":
        getName = request.form["name"]
        connection.execute(" DELETE FROM Book WHERE NAME='" + getName + "'")
        connection.commit()

        return redirect('/view')
    return render_template("delete.html")


@app.route('/update', methods=['GET', 'POST'])
def updation():
    global getNName
    cursor = connection.cursor()
    if request.method == "POST":
        getNName = request.form["name"]
        count = cursor.execute("SELECT * FROM Book WHERE NAME='" + getNName + "'")
        result = cursor.fetchall()
        if result is None:
            print("Book Name Not Exist")
        else:

            return render_template("update.html", search=result, status=True)


    else:

        return render_template("update.html", search=[], status=False)


@app.route('/up', methods=['GET', 'POST'])
def update_data():
    if request.method == "POST":
        getName = request.form["name"]
        getAu = request.form["auth"]
        getCat = request.form["cat"]
        getPrice = request.form["price"]
        getPub = request.form["pub"]

        connection.execute("UPDATE Book SET NAME='" + getName + "', AUTHOR='" + getAu + "'\
                            ,CATEGORY='" + getCat + "', PRICE='" + getPrice + "', PUBLISHER='" + getPub + "' \
                                  WHERE NAME='" + getNName + "'")
        connection.commit()
        print("Updated Successfully")
        return redirect('/view')
    return render_template("up.html")


if __name__ == "__main__":
    app.run(debug=True)