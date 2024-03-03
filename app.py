from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "0138"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Assuming you have a SQLite DB named 'users.db' with a table 'users' (id, username, password)
DATABASE = "user.db"


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    if user:
        return User(str(user["id"]), user["username"], user["password"])
    return None


# Redirect from the index to the login page
@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        if user and check_password_hash(user["password"], password):
            user_obj = User(str(user["id"]), user["username"], user["password"])
            login_user(user_obj)
            flash("You were successfully logged in")  # Flash a success message
            return redirect(url_for("dashboard", name=username))
        else:
            flash("Invalid username or password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    username = request.args.get(
        "name", "Unknown"
    )  # Default to 'Unknown' if 'name' not provided
    print("Received username:", username)
    return render_template("dashboard.html", username=username)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
