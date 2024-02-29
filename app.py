from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from flask_bcrypt import Bcrypt, check_password_hash
from flask_cors import CORS
import pickle
import sqlite3
import os
import warnings
warnings.filterwarnings('ignore')

# Configure app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# This configuration specifies the database file that the app will use to store and retrieve data
app.config['DATABASE'] = 'bigMart.db'

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create an instance of the Bcrypt extension for password hashing
bcrypt = Bcrypt(app)

# For session security
app.secret_key = os.urandom(24)

# loading the saved model
trained_model = pickle.load(open('C:/Users/ramee/Documents/FYP/sales_predictor.pkl', 'rb'))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        
        con = sqlite3.connect(app.config['DATABASE'])
        db = con.cursor()
        
        exist_user = db.execute("SELECT email, password, name FROM users WHERE email = ?", (email,))
        user_data = exist_user.fetchall()
        
        con.close()
        
        if user_data:
            user_data = user_data[0]

            if check_password_hash(user_data[1], password) and user_data[2] == name:
                session["name"] = user_data[2].capitalize()
                return redirect("/dashboard")
            else:
                session["login_failed"] = True

    return render_template("login.html")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/dashboard")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("Name")
        email = request.form.get("EMail")
        password = request.form.get("Password")
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        con = sqlite3.connect(app.config['DATABASE'])
        db = con.cursor()

        exist_email = db.execute("SELECT * FROM users WHERE email = ?", (email,))
        data3 = exist_email.fetchall()

        if  not data3:
            db.execute("INSERT INTO users (name, email, password) VALUES(?, ?, ?)", (name, email, hashed_password))
            
            con.commit()
            
            con.close()
            
            success = True
            return render_template("home.html", success=success)
        else:
            db.close()
            return render_template("user_exist.html")
        
    return render_template("register.html")


@app.route("/user_exist")
def user_exist():
    return render_template("user_exist.html")


@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if not session.get("name"):
        return redirect("/login")
    
    return render_template("dashboard.html")


if __name__ == '__main__':
    app.run(debug=True)